from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    user_id: int
    course_name: str

class EnrollmentUpdate(BaseModel):
    user_id: int
    course_name: str
    video_progress: int
    learning_hours: float
    is_completed: bool

class EnrollmentResponse(BaseModel):
    course_name: str
    video_progress: int
    is_completed: bool
    learning_hours: float

    class Config:
        orm_mode = True
