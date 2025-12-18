from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Quiz(Base):
    __tablename__ = "quizz"

    result_id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    score = Column(Integer)
    attempt_date = Column(String) 
