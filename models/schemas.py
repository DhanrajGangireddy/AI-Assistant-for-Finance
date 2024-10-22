from pydantic import BaseModel
from datetime import datetime
from typing import List

class QuestionInput(BaseModel):
    question: str


class AnswerOutput(BaseModel):
    answer: str
    suggestion: List[str]


class ChatHistory(BaseModel):
    status: str
    status_code: str
    data: AnswerOutput
