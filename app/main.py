from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.query_engine import run_query

from fastapi.responses import StreamingResponse
import io
import csv

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chat_history = []

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/", response_class=HTMLResponse)
async def post_ui(request: Request, question: str = Form(...)):
    try:
        result = run_query(question)
        # Smart format detection: list of dicts = table
        if isinstance(result, list) and all(isinstance(r, dict) for r in result):
            display_type = "table"
        else:
            display_type = "text"

        chat_history.append({"question": question, "answer": result, "type": display_type})

    except Exception as e:
        chat_history.append({"question": question, "answer": f"❌ Error: {str(e)}", "type": "text"})

    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})


@app.get("/download_csv")
async def download_csv():
    if not chat_history:
        return {"error": "No data available to download."}

    latest = chat_history[-1]
    if latest["type"] != "table":
        return {"error": "Latest response is not tabular."}

    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=latest["answer"][0].keys())
    writer.writeheader()
    writer.writerows(latest["answer"])
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=result.csv"}
    )