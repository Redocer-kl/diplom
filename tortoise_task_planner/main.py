import time
import asyncio
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import User, Task
from schemas import UserCreate, UserOut, TaskCreate, TaskOut, TaskUpdate
from config import init_db, TORTOISE_ORM

app = FastAPI()

# Инициализация Tortoise ORM
@app.on_event("startup")
async def startup():
    await init_db()

# Маршруты для пользователей
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    start_time = time.time()
    user_obj = await User.create(**user.dict())
    end_time = time.time()
    print(f"Create User Execution Time: {end_time - start_time} seconds")
    return UserOut(
        id=user_obj.id,
        username=user_obj.username,
        email=user_obj.email,
        created_at=user_obj.created_at,
    )

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    start_time = time.time()
    user = await User.get_or_none(id=user_id)
    end_time = time.time()
    print(f"Get User Execution Time: {end_time - start_time} seconds")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
    )

# Маршруты для задач
@app.post("/tasks/", response_model=TaskOut)
async def create_task(task: TaskCreate):
    start_time = time.time()
    user = await User.get_or_none(id=task.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task_obj = await Task.create(**task.dict(), user=user)
    end_time = time.time()
    print(f"Create Task Execution Time: {end_time - start_time} seconds")
    return TaskOut(
        id=task_obj.id,
        title=task_obj.title,
        description=task_obj.description,
        completed=task_obj.completed,
        created_at=task_obj.created_at,
        user_id=task_obj.user_id,
    )

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int):
    start_time = time.time()
    task = await Task.get_or_none(id=task_id)
    end_time = time.time()
    print(f"Get Task Execution Time: {end_time - start_time} seconds")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        user_id=task.user_id,
    )

@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task_update: TaskUpdate):
    start_time = time.time()
    task = await Task.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = task_update.completed
    await task.save()
    end_time = time.time()
    print(f"Update Task Execution Time: {end_time - start_time} seconds")
    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
        user_id=task.user_id,
    )

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    start_time = time.time()
    task = await Task.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await task.delete()
    end_time = time.time()
    print(f"Delete Task Execution Time: {end_time - start_time} seconds")
    return {"message": "Task deleted successfully"}

# Маршрут для массового создания задач (тестирование производительности)
@app.post("/tasks/bulk_create/")
async def bulk_create_tasks():
    start_time = time.time()
    user = await User.create(username="test_user", email="test@example.com")
    tasks = [Task(title=f"Task {i}", description=f"Description {i}", user=user) for i in range(1000)]
    await Task.bulk_create(tasks)
    end_time = time.time()
    print(f"Bulk Create Tasks Execution Time: {end_time - start_time} seconds")
    return {"message": "1000 tasks created successfully"}

# Регистрация Tortoise ORM в FastAPI
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)