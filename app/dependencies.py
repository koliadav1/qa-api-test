from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import services

# Получение вопроса по id
def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):
    question = services.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return question

# Получение ответа по id
def get_answer_by_id(
    answer_id: int,
    db: Session = Depends(get_db)
):
    answer = services.get_answer(db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return answer