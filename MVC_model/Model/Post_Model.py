
# Define Post model
class Post(BaseModel):
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime


