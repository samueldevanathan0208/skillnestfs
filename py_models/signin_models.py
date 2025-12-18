from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String)
    user_password = Column(String)
    user_dateofbirth = Column(String)
    user_phone = Column(String)
    user_gender = Column(String)
