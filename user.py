from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db_depends import get_db
from typing import Annotated
from models.user import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, text

router = APIRouter(prefix='/user', tags=['users'])
DBSession = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_users(db: DBSession):
    users = db.execute(text("SELECT id, username, firstname, lastname, age FROM users"))
    list_of_all_users = []
    for user in users:
        user = {'id': user.id,'username': user.username, 'firstname': user.firstname,
                'lastname': user.lastname, 'age': user.age}
        list_of_all_users.append(user)
    return list_of_all_users


@router.post('/create')
async def create_user(db: DBSession, create_new_user: CreateUser):
    db.execute(insert(User).values(username=create_new_user.username,
                                   firstname=create_new_user.firstname,
                                   lastname=create_new_user.lastname,
                                   age=create_new_user.age))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/user_id')
async def user_by_id(db: DBSession, user_id: int):
    users = db.execute(text("SELECT id, username, firstname, lastname, age FROM users"))
    list_of_all_users = []
    for user in users:
        if user.id == user_id:
            user = {'id': user.id, 'username': user.username, 'firstname': user.firstname,
                        'lastname': user.lastname, 'age': user.age}
            list_of_all_users.append(user)
            return list_of_all_users
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

@router.get('/user_id/tasks')
async def task_by_user_id(db: DBSession, user_id: int):
    task = db.execute(text("SELECT * FROM task WHERE user_id = :user_id"),
                      {'user_id': user_id}).fetchone()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    return [task.id, task.title, task.content, task.priority]

@router.put('/update')
async def update_user(db: DBSession,
                      user_update: UpdateUser, user_id: int):
    user = db.execute(text("SELECT * FROM users WHERE id = :id"),
                       {'id': user_id}).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    update_query = text(
        'UPDATE users SET firstname = :firstname, lastname = :lastname, age = :age WHERE id = :id')
    db.execute(update_query,
               {'id': user_id, 'firstname': user_update.firstname,
                'lastname': user_update.lastname, 'age': user_update.age},)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update successful!'}


@router.delete('/delete')
async def delete_user(db: DBSession, user_id):
    user = db.execute(text("SELECT * FROM users WHERE id = :id"),
                      {'id': user_id}).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    delete_query = text(
        'DELETE FROM users WHERE id = :id')
    db.execute(delete_query,
               {'id': user_id}, )
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update successful!'}
