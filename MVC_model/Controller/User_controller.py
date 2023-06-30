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
