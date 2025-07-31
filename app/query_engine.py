import os
import re
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from sqlalchemy import text

#from app.db import get_db_connection  # adjust if needed
from app.db import langchain_db
from app.db import engine
# pass `langchain_db` to your SQLChain or agent

from app.utils import clean_sql_query  # your existing utility

from dotenv import load_dotenv
load_dotenv()

def strip_values_recursive(obj):
    if isinstance(obj, dict):
        return {k: strip_values_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [strip_values_recursive(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(strip_values_recursive(v) for v in obj)
    else:
        return ""  # strip leaf values

def get_table_description_with_sample(db, table_name):
    try:
        usable_tables = db.get_usable_table_names()
        if table_name not in usable_tables:
            raise Exception(f"Table '{table_name}' not found")

        schema = db.get_table_info([table_name])

        # Get columns
        column_query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """
        columns = [row[0] for row in db.run(column_query)]

        # Get sample row
        sample_row_result = db._execute(f"SELECT * FROM {table_name} LIMIT 1;")
        row_dict = dict(zip(columns, sample_row_result)) if sample_row_result else {}
        stripped_sample = strip_values_recursive(row_dict)

        return f"### Table: {table_name}\n\n{schema}\n\nSample Row Structure:\n{str(stripped_sample)}"
    except Exception as e:
        return f"### Table: {table_name}\n\nError: {str(e)}"

def strip_sample_rows(description: str) -> str:
    # Remove anything starting from /* to */
    return re.sub(r'/\*.*?\*/', '', description, flags=re.DOTALL)


def run_query(question: str):
    print("inside run query ;;; ",question)
    db = langchain_db
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        openai_api_key=os.getenv("MYOPENAI_API_KEY")
    )

    # Step 1: Detect relevant tables
    usable_tables = db.get_usable_table_names()
    table_names_str = "\n".join(usable_tables)

    table_detection_prompt = f"""
You are a PostgreSQL assistant.
Given a user question and a list of available table names, identify all the relevant tables from the list that are needed to answer the question.

Return only a **comma-separated list** of table names. Do not add SQL code or explanation.

Available Tables:
{table_names_str}

User Question:
{question}

Relevant Table Names (comma-separated):
"""

    detected_tables_str = llm.invoke(table_detection_prompt).content.strip()
    detected_tables = [t.strip() for t in re.split(r'[,\n]+', detected_tables_str) if t.strip()]
    modified_question = f"{question.strip()} using tables: {', '.join(detected_tables)}"

    # Step 2: Collect schemas + sample row for each relevant table
    all_descriptions = [
        get_table_description_with_sample(db, table) for table in detected_tables
    ]
    combined_table_info = "\n\n".join(all_descriptions)
    combined_table_info=strip_sample_rows(combined_table_info)

    #print("---------- combined_table_info  ::: ",combined_table_info)
    # Step 3: Generate SQL from prompt
    prompt = PromptTemplate(
        input_variables=["question", "table_info"],
        template="""
You are an expert PostgreSQL developer.

Use the following table schema(s) and sample row structure(s) to generate an SQL query for the given question.

Table info:
{table_info}

User Question: {question}

SQLQuery:
"""
    )

    chain = prompt | llm
    result = chain.invoke({
        "question": modified_question,
        "table_info": combined_table_info
    })

    raw_sql = result.content.strip()
    sql_query = clean_sql_query(raw_sql)

    # Execute SQL and return results as list of dicts
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        columns = result.keys()
        rows = result.fetchall()
        result_dicts = [dict(zip(columns, row)) for row in rows]

        return result_dicts, sql_query

