from pydantic import BaseModel

# Tạo class User
class User(BaseModel):
    user_id: int
    username: str
    phone_number: int
    address: str

