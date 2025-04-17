from pydantic import BaseModel
from typing import List, Optional


class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]


class QuizStartResponse(BaseModel):
    attempt_id: int
    questions: List[QuizQuestion]


class QuizAnswer(BaseModel):
    question_id: int
    answer: Optional[str]  # None or "" means unattempted


class QuizSubmitRequest(BaseModel):
    attempt_id: int
    category_id: int
    answers: List[QuizAnswer]


class QuizSubmitResponse(BaseModel):
    attempt_id: int
    total_questions: int
    questions_attempted: int
    questions_unattempted: int
    correct_answers: int
    wrong_answers: int
    score: int


class QuizAttemptResponse(BaseModel):
    id: int
    user_id: int
    attempt_id: int
    category_id: int
    total_questions: int
    questions_attempted: int
    questions_unattempted: int
    correct_answers: int
    score: int

    class Config:
        orm_mode = True
