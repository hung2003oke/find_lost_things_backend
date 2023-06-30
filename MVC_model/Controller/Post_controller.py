
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