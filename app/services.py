from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int) -> Optional[models.Question]:
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
    db_question = models.Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info(f"Создан вопрос с ID: {db_question.id}")
    return db_question

def delete_question(db: Session, question_id: int) -> bool:
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question:
        db.delete(question)
        db.commit()
        logger.info(f"Удален вопрос с ID: {question_id}")
        return True
    return False

def get_answers_for_question(db: Session, question_id: int) -> List[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()

def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int) -> models.Answer:
    db_answer = models.Answer(
        text=answer.text,
        user_id=answer.user_id,
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    logger.info(f"Создан ответ с ID: {db_answer.id} для вопроса с ID: {question_id}")
    return db_answer

def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def delete_answer(db: Session, answer_id: int) -> bool:
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer:
        db.delete(answer)
        db.commit()
        logger.info(f"Удален ответ с ID: {answer_id}")
        return True
    return False