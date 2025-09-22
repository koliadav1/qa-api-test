from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    user_id: str = Field(..., min_length=1)

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionWithAnswers(Question):
    answers: List[Answer] = []