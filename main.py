from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from uvicorn import run as run_server
from typing import Optional
import psycopg2


app = FastAPI()

# Tạo class User
class User(BaseModel):
    user_id: int
    username: str
    phone_number: int
    address: str

# Cơ sở dữ liệu của user
users = [
    User(user_id=1, username="David", phone_number=123456789, address="Ha Noi"),
    User(user_id=2, username="Johnathan", phone_number=7777777, address="Hai Phong")
]

# Define Post model
class Post(BaseModel):
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime

# Cơ sở dữ liệu của bài đăng
posts = [
    Post(post_id=11, user_id=1, content="Arsenal vo dich C1", created_at=datetime.now(), updated_at=datetime.now()),
    Post(post_id=12, user_id=2, content="ManCity vo dich C1", created_at=datetime.now(), updated_at=datetime.now()),
    Post(post_id=13, user_id=1, content="Toi di hoc", created_at=datetime.now(), updated_at=datetime.now()),
]

# Lấy danh sách tất cả bài đăng
# khi muốn truyền vào 1 id, viết đường dẫn như thế này: /<tên đối tượng số nhiều>/<id của đối tượng>/
@app.get('/users/{user_id}/posts')
def lay_bai_dang(user_id: int):
    user_posts = [post for post in posts if post.user_id == user_id]
    return {'posts': user_posts}

# Lấy chi tiết 1 bài đăng
@app.get('/posts/{post_id}')
def lay_bai_dang(post_id: int):
    detail_post = None
    for post in posts:
        if post.post_id == post_id:
            detail_post = post

    if detail_post == None:
        return {'error': True}
    else:
        return detail_post

# Create Post
@app.post("/posts/")
def create_content(content: Post, user_id: int):
    user = next((u for u in users if u.user_id == user_id), None)
    if user and user.user_id == 2:
        content.created_at = datetime.now()
        posts.append(content)
        return {"message": "Content created"}
    return {"error": "User not authorized to create content"}

# Update Post
@app.put("/posts/{post_id}/content")
async def update_content(post_id: int, content: Post):
    for i, p in enumerate(posts):
        if p.post_id == post_id:
            content.updated_at = datetime.now()
            posts[i] = content
            return {"message": "Content updated successfully"}
    return {"error": "Can't update content"}

# Delete Post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for i, p in enumerate(posts):
        if p.post_id == post_id:
            del posts[i]
            return {"message": "Content deleted successfully"}
    return {"error": "Can't delete content"}

############# Phần USER

# Tạo user mới
@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created successfully"}

# Lấy chi tiết thông tin của một user
@app.get("/users/{user_id}")
def lay_chitiet_user(user_id: int):
    detail_user = next((u for u in users if u.user_id == user_id), None)
    if detail_user is None:
        return {"error": True}
    else:
        return detail_user

# Sửa số điện thoại của user
@app.put("/users/{user_id}/phone_number")
def update_phone_number(user_id: int, phone_number: int):
    for user in users:
        if user.user_id == user_id:
            user.phone_number = phone_number
            return {"message": "Phone number of user updated successfully"}
    return {"error": "Can't update phone number"}

# Sửa địa chỉ của user
@app.put("/users/{user_id}/address")
def update_address(user_id: int, address: str):
    for user in users:
        if user.user_id == user_id:
            user.address = address
            return {"message": "Address of user updated successfully"}
    return {"error": "Can't update address"}

# Sửa tên của user
@app.put("/users/{user_id}/username")
def update_username(user_id: int, username: str):
    for user in users:
        if user.user_id == user_id:
            user.username = username
            return {"message": "Username of user updated successfully"}
    return {"error": "Can't update username"}

# Xóa user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.user_id == user_id:
            del users[i]
            return {"message": "Delete user complete"}
    return {"error": "Can't delete user"}

# Chạy FastAPI server
if __name__ == "__main__":
    run_server(app, host="127.0.0.1", port=8000)
