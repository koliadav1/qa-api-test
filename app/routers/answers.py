from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app import schemas, database, dependencies, services
from app.models import Answer

router = APIRouter()

# Добавление ответа на вопрос
@router.post("/questions/{question_id}", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int = Path(..., gt=0),
    answer: schemas.AnswerCreate = ...,
    db: Session = Depends(database.get_db)
):
    dependencies.get_question_by_id(question_id, db)
    
    return services.create_answer(db=db, answer=answer, question_id=question_id)

# Получение ответа по id
@router.get("/{answer_id}", response_model=schemas.Answer)
def read_answer(
    answer: Answer = Depends(dependencies.get_answer_by_id)
):
    return answer

# Удаление ответа
@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    answer_id: int, 
    db: Session = Depends(database.get_db)
):
    if not services.delete_answer(db, answer_id=answer_id):
        raise HTTPException(status_code=404, detail="Answer not found")
    return None