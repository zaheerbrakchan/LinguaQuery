# LinqueQuery 🧠🔍

**LinqueQuery** is an open-source project that translates natural language questions into SQL queries using LangChain and LLMs (like OpenAI or Azure OpenAI). Designed to work with structured data from sources like **PostgreSQL**, **MongoDB**, and **Elasticsearch**, LinqueQuery helps non-technical users query complex datasets effortlessly.

---

## 🚀 Features

- 🗣️ Natural language → SQL conversion
- 🔗 Supports **PostgreSQL** (MongoDB, ElasticSearch coming soon)
- 🧠 Powered by **LangChain** + OpenAI / Azure OpenAI
- ⚡ FastAPI backend for easy deployment
- 🧩 Extensible for multi-database use cases
- 🛠️ Easy to plug into dashboards or internal tools

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

