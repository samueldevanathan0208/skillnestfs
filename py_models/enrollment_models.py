from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    course_name = Column(String) 
    video_progress = Column(Integer, default=0) 
    is_completed = Column(Boolean, default=False)
    learning_hours = Column(Float, default=0.0)
    
    user = relationship("User")
