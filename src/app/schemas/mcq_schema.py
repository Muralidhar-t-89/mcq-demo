from datetime import datetime
from pydantic import BaseModel, model_validator
from typing import List


class MCQCreate(BaseModel):
    question: str
    options: List[str]
    correct_option: List[str]
    category: str
    created_by: int
    created_date: datetime

    @model_validator(mode='before')
    def check_correct_option(cls, values):
        options = values.get('options')
        correct_option = values.get('correct_option')
        if correct_option and not set(correct_option).issubset(options):
            raise ValueError("correct_option must be a subset of options")
        return values

    class Config:
        orm_mode = True


class MCQUpdate(BaseModel):
    question: str
    options: List[str]
    correct_option: List[str]
    category: str
    created_by: int
    created_date: datetime

    @model_validator(mode='before')
    def check_correct_option(cls, values):
        options = values.get('options')
        correct_option = values.get('correct_option')
        if correct_option and not set(correct_option).issubset(options):
            raise ValueError("correct_option must be a subset of options")
        return values

    class Config:
        orm_mode = True


class MCQ(MCQCreate):
    id: int

    class Config:
        orm_mode = True

