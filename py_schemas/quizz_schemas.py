from pydantic import BaseModel

class CreateQuiz(BaseModel):
    result_id: int
    quiz_id: int
    user_id: int
    score: int
    attempt_date: str
