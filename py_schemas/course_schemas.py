from pydantic import BaseModel

class Create_course(BaseModel):
    course_id: int
    title: str
    description: str
    category: str
    level: str
    created_by: int
    created_at: str
