from pydantic import BaseModel, EmailStr

class GetTokenSchema(BaseModel):
    email: EmailStr
    password: str
