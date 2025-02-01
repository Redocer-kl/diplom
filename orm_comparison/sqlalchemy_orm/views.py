from django.shortcuts import render, redirect
from .database import get_db
from .models import User, Task
from .forms import RegistrationForm, LoginForm, TaskForm
from django.contrib import messages
import time

def register(request):
    start_time = time.time()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            db = next(get_db())
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            db.add(user)
            db.commit()
            messages.success(request, 'Registration successful!')
            return redirect('sa_login')
    else:
        form = RegistrationForm()
    end_time = time.time()
    print(f"Register sa: {end_time - start_time}")
    return render(request, 'sqlalchemy_orm/register.html', {'form': form})

def login(request):
    start_time = time.time()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            db = next(get_db())
            user = db.query(User).filter_by(username=form.cleaned_data['username']).first()
            if user and user.check_password(form.cleaned_data['password']):
                request.session['user_id'] = user.id  # Используем Django-сессии
                return redirect('sa_task_list')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    end_time = time.time()
    print(f"Login sa: {end_time - start_time}")
    return render(request, 'sqlalchemy_orm/login.html', {'form': form})

def task_list(request):
    start_time = time.time()
    if 'user_id' not in request.session:
        return redirect('sa_login')
    db = next(get_db())
    tasks = db.query(Task).filter_by(user_id=request.session['user_id']).all()
    end_time = time.time()
    print(f"Tasklist sa: {end_time - start_time}")
    return render(request, 'sqlalchemy_orm/task_list.html', {'tasks': tasks, })

def add_task(request):
    start_time = time.time()
    if 'user_id' not in request.session:
        return redirect('sa_login')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            db = next(get_db())
            task = Task(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user_id=request.session['user_id']
            )
            db.add(task)
            db.commit()
            return redirect('sa_task_list')
    else:
        form = TaskForm()
    end_time = time.time()
    print(f"Add task sa: {end_time - start_time}")
    return render(request, 'sqlalchemy_orm/add_task.html', {'form': form})


def toggle_task(request, task_id):

    if 'user_id' not in request.session:
        return redirect('sa_login')

    start_time = time.time()
    db = next(get_db())
    task = db.query(Task).filter_by(id=task_id, user_id=request.session['user_id']).first()

    if not task:
        messages.error(request, 'Task not found')
        return redirect('sa_task_list')

    task.toggle_complete()
    db.commit()
    end_time = time.time()
    print(f"Toggle sa: {end_time - start_time}")
    return redirect('sa_task_list')


def delete_task(request, task_id):
    if 'user_id' not in request.session:
        return redirect('sa_login')
    start_time = time.time()
    db = next(get_db())
    task = db.query(Task).filter_by(id=task_id, user_id=request.session['user_id']).first()

    if not task:
        messages.error(request, 'Task not found')
        return redirect('sa_task_list')

    task.delete(db)
    db.commit()
    end_time = time.time()
    print(f"Delete sa: {end_time - start_time}")
    return redirect('sa_task_list')