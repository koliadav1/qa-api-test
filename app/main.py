import os
from fastapi import FastAPI
if os.getenv("TESTING") != "True":
    from app.database import engine
    from app.models import Base
from app.routers import questions, answers
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if os.getenv("TESTING") != "True":
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Question Answer API",
    description="API для вопросов и ответов",
    version="1.0.0"
)

app.include_router(questions.router, prefix="/questions", tags=["Вопросы"])
app.include_router(answers.router, prefix="/answers", tags=["Ответы"])