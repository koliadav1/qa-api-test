from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app import schemas, database, dependencies, services
from typing import List
from app.models import Question

router = APIRouter()

# Получение списка вопросов
@router.get("/", response_model=List[schemas.Question])
def read_questions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    questions = services.get_questions(db, skip=skip, limit=limit)
    for question in questions:
        question.answers_count = len(question.answers)
    return questions

# Добавление вопроса
@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(
    question: schemas.QuestionCreate, 
    db: Session = Depends(database.get_db)
):
    return services.create_question(db=db, question=question)

# Получение вопроса и списка ответов на него
@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def read_question(
    question: Question = Depends(dependencies.get_question_by_id)
):
    return question

# Удаление вопроса и всех ответов к нему (каскадно)
@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int, 
    db: Session = Depends(database.get_db)
):
    if not services.delete_question(db, question_id=question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return None

# Добавление ответа на вопрос
@router.post("/{question_id}/answers", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int = Path(..., gt=0),
    answer: schemas.AnswerCreate = ...,
    db: Session = Depends(database.get_db)
):
    dependencies.get_question_by_id(question_id, db)
    
    return services.create_answer(db=db, answer=answer, question_id=question_id)