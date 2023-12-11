from fastapi import APIRouter, Body, HTTPException, Depends
from models.model import Main_User, Main_UserDB, New_Response
from typing import List, Annotated, Union

#Роутер
router = APIRouter()

#бд
db = []

#Класс с методами операций над пользователями
class UserMethods:
# Методы для выполнения операций CRUD
    @classmethod
    def get_user(cls, id: int):
        for user in db:
            if user['id'] == id:
                return user
        return New_Response(message="Пользователь не найден!")


    @classmethod
    def get_all_users(cls):
        return db


    @classmethod
    def create_user(cls, user: Annotated[Main_User, Body(embed=True, description="Новый пользователь")]):
        user_data = user.model_dump()
        db.append(user_data)
        return user_data


    @classmethod
    def update_user(cls, id: int, user: Main_User):
        current_user = UserMethods.get_user(id)
        if type(current_user) is New_Response:
            return New_Response(message="Пользователь не найден!")
        current_user.update(user.model_dump())
        return current_user


    @classmethod
    def delete_user(cls, id: int):
        user = UserMethods.get_user(id)
        if type(user) is New_Response:
            return New_Response(message="Пользователь не найден!")
        db.remove(user)
        return user

@router.get("/api/users", response_model=Union[List[Main_User], None])
async def get_users():
    return UserMethods.get_all_users()

@router.post("/api/users", response_model=Union[Main_User, New_Response])
async def create_user(user: Main_User):
    return UserMethods.create_user(user)

@router.put("/api/users", response_model=Union[Main_User, New_Response])
async def edit_person(id: int, user: Main_User):
    return UserMethods.update_user(id, user)

@router.get("/api/users/{id}", response_model=Union[Main_User, New_Response])
async def get_user(id: int):
    return UserMethods.get_user(id)

@router.delete("/api/users/{id}", response_model=Union[Main_User, New_Response])
async def delete_user(id: int):
    return UserMethods.delete_user(id)
