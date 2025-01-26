from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db_depends import get_db
from typing import Annotated
from models.task import Task
from models.user import User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, text


router = APIRouter(prefix='/task', tags=['task'])
DBSession = Annotated[Session, Depends(get_db)]


@router.get('/')
async def all_task(db: DBSession):
    tasks = db.execute(text("SELECT id, title, content, priority, user_id, slug FROM task"))
    list_of_all_tasks = []
    for task in tasks:
        task = {'id': task.id, 'title': task.title, 'content': task.content,
                'priority': task.priority,
                'user_id': task.user_id, 'slug': task.slug}
        list_of_all_tasks.append(task)
    return list_of_all_tasks

@router.get('task_id')
async def task_id(db: DBSession, id_task: int):
    tasks = db.execute(text("SELECT id, title, content, priority, user_id, slug FROM task"))
    list_of_all_tasks = []
    for task in tasks:
        if task.id == id_task:
            task = {'id': task.id, 'title': task.title, 'content': task.content,
                'priority': task.priority,
                'user_id': task.user_id, 'slug': task.slug}
            list_of_all_tasks.append(task)
            return list_of_all_tasks
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')

@router.post('/create')
async def create_task(db: DBSession, task_create: CreateTask, user_id: int):
    user = db.execute(text("SELECT * FROM users WHERE id = :user_id"),
                      {'user_id': user_id}).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(insert(Task).values(title=task_create.title,
                                   content=task_create.content,
                                   priority=task_create.priority,
                                   user_id=user_id))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put('/update')
async def update_task(db: DBSession, id_task: int, task_update: UpdateTask):
    task = db.execute(text("SELECT * FROM task WHERE id = :id"),
                      {'id': id_task}).fetchone()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    update_query = text(
        'UPDATE task SET title = :title, content = :content, priority = :priority '
        'WHERE id = :id')
    db.execute(update_query,
               {'id': id_task, 'title': task_update.title,
                'content': task_update.content, 'priority': task_update.priority}, )
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'task update successful!'}

@router.delete('/delete')
async def delete_task(db: DBSession, id_task: int):
    task = db.execute(text("SELECT * FROM task WHERE id = :id"),
                      {'id': id_task}).fetchone()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    delete_query = text(
        'DELETE FROM task WHERE id = :id')
    db.execute(delete_query,
               {'id': id_task},)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'task delete successful!'}
