from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

import explanation_module
import learning_path
import qna
import quiz_module
import summary_module

from models import (
    ExplainRequest,
    LearningPathRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
)


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="2.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.get("/qa")
async def qa_get(question: str):
    try:
        answer = qna.answer_question(question)
        return {"question": question, "answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/qa")
async def qa_post(payload: QARequest):
    try:
        answer = qna.answer_question(payload.question)
        return {"question": payload.question, "answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        explanation = explanation_module.explain_topic(payload.topic)
        return {"topic": payload.topic, "explanation": explanation}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        result = quiz_module.generate_quiz(payload.text)
        return result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    try:
        summary = summary_module.summarize_text(payload.text)
        return {"summary": summary}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/learn/recommendations")
async def learning_recommendations(topic: str, level: str = "beginner"):
    try:
        recommendations = learning_path.get_learning_recommendations(topic, level)
        return {"topic": topic, "level": level, "recommendations": recommendations}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
async def learning_recommendations_post(payload: LearningPathRequest):
    try:
        recommendations = learning_path.get_learning_recommendations(payload.topic, payload.level)
        return {"topic": payload.topic, "level": payload.level, "recommendations": recommendations}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
