import re

def clean_sql_query(query: str) -> str:
    query = re.sub(r"^(SQLQuery:|Answer:)\s*", "", query.strip(), flags=re.IGNORECASE)
    query = query.split(";")[0] + ";" if ";" in query else query.strip()
    query = query.replace("sql", "").strip()
    return query
