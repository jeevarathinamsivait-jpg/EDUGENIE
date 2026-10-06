from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import TaskRequest, TaskResponse

from modules.qna import answer_question
from modules.explanation import explain_topic
from modules.quiz import generate_quiz
from modules.summary import summarize_text
from modules.learning_path import get_learning_recommendations

from services.gemini_service import GeminiServiceError


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Health check
@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# Common task handler
def run_task(task: str, text: str):

    try:

        if task == "qa":

            result = answer_question(text)

        elif task == "explain":

            result = explain_topic(text)

        elif task == "quiz":

            result = generate_quiz(text)

        elif task == "summarize":

            result = summarize_text(text)

        elif task == "learn":

            result = get_learning_recommendations(text)

        else:

            raise HTTPException(
                status_code=400,
                detail="Unknown task."
            )

        return TaskResponse(
            task=task,
            result=result
        )

    except GeminiServiceError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {error}"
        )


# Q&A API
@app.post("/qa", response_model=TaskResponse)
def qa(payload: TaskRequest):

    return run_task(
        "qa",
        payload.text
    )


# Explanation API
@app.post("/explain", response_model=TaskResponse)
def explain(payload: TaskRequest):

    return run_task(
        "explain",
        payload.text
    )


# Quiz API
@app.post("/quiz", response_model=TaskResponse)
def quiz(payload: TaskRequest):

    return run_task(
        "quiz",
        payload.text
    )


# Summary API
@app.post("/summarize", response_model=TaskResponse)
def summarize(payload: TaskRequest):

    return run_task(
        "summarize",
        payload.text
    )


# Learning path API
@app.post(
    "/learn/recommendations",
    response_model=TaskResponse
)
def learning_path(payload: TaskRequest):

    return run_task(
        "learn",
        payload.text
    )