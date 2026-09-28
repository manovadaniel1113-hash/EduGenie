from pydantic import BaseModel, Field


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = Field(default="beginner")


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResult(BaseModel):
    topic: str
    questions: list[QuizQuestion]
