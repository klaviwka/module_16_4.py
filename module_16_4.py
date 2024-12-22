from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, conint
from typing import List

app = FastAPI()

# Список пользователей
users: List[BaseModel] = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: constr(min_length=1)  # Имя пользователя не должно быть пустым
    age: conint(ge=18, le=120)  # Возраст от 18 до 120

# Получение списка всех пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users

# Создание нового пользователя
@app.post("/user/{username}/{age}", response_model=User, response_description="Пользователь зарегистрирован")
async def create_user(username: str, age: int):
    user_id = len(users) + 1  # Генерация id
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# Обновление существующего пользователя
@app.put("/user/{user_id}", response_model=User, response_description="Пользователь обновлен")
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# Удаление пользователя
@app.delete("/user/{user_id}", response_description="Пользователь удален")
async def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")
