from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    level = Column(String)
    create_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(String)

    author = relationship("User")
