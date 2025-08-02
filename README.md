# LinqueQuery 🧠🔍

**LinqueQuery** is a full-stack, open-source solution that enables users to query structured databases using natural language. More than just a text-to-SQL converter, LinqueQuery dynamically introspects your database schema, intelligently selects relevant tables, generates accurate SQL, executes the query, and displays the results in an intuitive UI — with an option to download them as CSV.

It is designed to work with diverse structured data sources such as **PostgreSQL**, **MongoDB**, and **Elasticsearch**, making it ideal for business analysts, healthcare teams, and anyone who wants to explore their data without writing complex queries.


---

## 🚀 Features

- 🔍 Natural language to end-to-end query results  
- 🧠 Dynamic schema introspection to select correct tables/columns  
- 📄 Auto-generates and runs SQL queries from plain English  
- 📊 Displays results directly in the UI  
- ⬇️ CSV download support for query results  
- 🔗 Supports **PostgreSQL** (MongoDB, ElasticSearch coming soon)  
- ⚡ FastAPI backend with LangChain + OpenAI / Azure OpenAI  
- 🧩 Easily extensible to new data sources  

---

## 📦 Tech Stack

- **Backend**: Python, FastAPI  
- **LLM Layer**: LangChain, OpenAI / Azure OpenAI  
- **Databases**: PostgreSQL (more in progress)  
- **Others**: SQLAlchemy, Pydantic, Dotenv

---

## 🧠 Example

**Query:**

> "Show me all patients diagnosed with diabetes in the last 6 months."

**Output:**
```sql
SELECT name, diagnosis_date 
FROM patients 
WHERE diagnosis = 'diabetes' 
  AND diagnosis_date >= CURRENT_DATE - INTERVAL '6 months';
```




⚙️ Getting Started
1. Clone the repo

      git clone https://github.com/zaheerbrakchan/LinguaQuery
  
      cd linquequery

   

3. Install dependencies
   
      pip install -r requirements.txt
   


5. Add your .env file
   
     Create a .env file in the root directory and configure:

     OPENAI_API_KEY=your_api_key

     DATABASE_URL=postgresql://user:password@localhost:5432/yourdb



4. Run the app
   
     uvicorn app.main:app --reload

     Then go to http://localhost:8000/docs to explore the API.



📌 Roadmap
✅ PostgreSQL support

🕒 Elasticsearch & MongoDB support

🕒 UI-based query builder

🕒 Query caching and optimization

🕒 Schema introspection and auto docs



🤝 Contributing
Pull requests are welcome!
Fork the repo
Create a new branch: feature/your-feature-name
Make your changes
Submit a Pull Request
Please write clear commit messages and follow standard Python formatting.



📄 License
This project is licensed under the MIT License.



🙋 Contact
Zaheer Abass
📧 xaheer3scc@gmail.com
🌐 [LinkedIn](https://www.linkedin.com/in/zaheer-abass-590a31142/)


If you like the project, please ⭐ the repo and share it with others!

