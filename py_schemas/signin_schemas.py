from pydantic import BaseModel

class CreateUser(BaseModel):
    user_name: str
    user_email: str
    user_password: str
    user_dateofbirth: str
    user_phone: str
    user_gender: str
