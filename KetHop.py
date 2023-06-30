from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import psycopg2
from sqlalchemy.orm import Session

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

# Hàm để thêm danh sách users vào cơ sở dữ liệu
def add_users_to_database(db: Session, users):
    for user in users:
        db.add(user)
    db.commit()



def add_posts_to_database(db: Session, posts):
    for post in posts:
        db.add(post)
    db.commit()

# Lấy danh sách tất cả bài đăng
# khi muốn truyền vào 1 id, viết đường dẫn như thế này: /<tên đối tượng số nhiều>/<id của đối tượng>/
@app.get('/users/{user_id}/posts')
def lay_bai_dang(user_id: int):
    con=connect_to_db()
    cursor=con.cursor()
    cursur.excute("SELECT *FROM posts WHERE user_id=%s ",(user_id) )
    post_data=cursor.fetchone()
    cursor.close()
    con.close()
    if post_data:
        post = Post(
            user_id=user_data[0],
            post_id=user_data[1],
            content=user_data[2],
            created_at=user_data[3],
            updated_at=user_data[4]
        )
        return post
    else:
        return {"error": "Post not found"}
    return {'posts': user_posts}

# Lấy chi tiết 1 bài đăng
@app.get('/posts/{post_id}')
def lay_bai_dang(post_id: int):
    con = connect_to_db()
    cursor = con.cursor()
    cursur.excute("SELECT *FROM Post WHERE post_id=%s ", (post_id))
    post_data = cursor.fetchone()
    cursor.close()
    con.close()
    if post_data:
        post = Post(
            user_id=user_data[0],
            post_id=user_data[1],
            content=user_data[2],
            created_at=user_data[3],
            updated_at=user_data[4]
        )
        return post
    else:
        return {"error": "Post not found"}
    return {'Post': user_posts}
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

# Kết nối đến cơ sở dữ liệu PostgreSQL
def connect_to_db():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="hung2003",
        host="127.0.0.1",
        port="5432"
    )
    return con

# Tạo user mới
@app.post("/users")
def create_user(user: User):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, username, phone_number, address) VALUES (%s, %s, %s, %s)",
        (user.user_id, user.username, user.phone_number, user.address)
    )
    con.commit()
    cursor.close()
    con.close()
    return {"message": "User created successfully"}

# Lấy chi tiết thông tin của một user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    con.close()
    if user_data:
        user = User(
            user_id=user_data[0],
            username=user_data[1],
            phone_number=user_data[2],
            address=user_data[3]
        )
        return user
    else:
        return {"error": "User not found"}

# Sửa số điện thoại của user
@app.put("/users/{user_id}/phone_number")
def update_phone_number(user_id: int, phone_number: int):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("UPDATE users SET phone_number = %s WHERE user_id = %s", (phone_number, user_id))
    con.commit()
    cursor.close()
    con.close()
    return {"message": "Phone number of user updated successfully"}

# Xóa user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    con.commit()
    cursor.close()
    con.close()
    return {"message": "User deleted successfully"}

# Chạy FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
