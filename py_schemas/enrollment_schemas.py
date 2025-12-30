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
    completed_videos: str = "[]"

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_name: str
    video_progress: int
    is_completed: bool
    learning_hours: float
    completed_videos: str = "[]"
    certificate_id: str = None

    class Config:
        from_attributes = True
