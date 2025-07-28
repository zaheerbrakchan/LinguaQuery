from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.query_engine import run_query
import io
import csv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Maintain chat history (limit to last 5 if needed)
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })

@app.post("/", response_class=HTMLResponse)
async def post_ui(request: Request, question: str = Form(...)):
    try:
        result, sql_query = run_query(question)
        print("sql_query :::: ",sql_query)

        if isinstance(result, list) and all(isinstance(r, dict) for r in result):
            display_type = "table"
        else:
            display_type = "text"

        new_chat = {
            "question": question,
            "answer": result,
            "type": display_type,
            "sql": sql_query
        }

    except Exception as e:
        new_chat = {
            "question": question,
            "answer": f"❌ Error: {str(e)}",
            "type": "text",
            "sql": None
        }

    # Keep only the latest one
    chat_history.clear()
    chat_history.append(new_chat)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_history": chat_history
    })

@app.get("/download_csv")
async def download_csv():
    if not chat_history or chat_history[0].get("type") != "table":
        return {"error": "No tabular data available to download."}

    latest_table = chat_history[0]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=latest_table["answer"][0].keys())
    writer.writeheader()
    writer.writerows(latest_table["answer"])
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=result.csv"}
    )
