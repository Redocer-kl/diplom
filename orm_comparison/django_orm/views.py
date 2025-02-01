from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, RegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
import time

def register(request):
    start_time = time.time()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически войти после регистрации
            return redirect('task_list')
    else:
        form = RegistrationForm()
    end_time = time.time()
    print(f"Register: {end_time - start_time}")
    return render(request, 'register.html', {'form': form})

@login_required
def task_list(request):
    start_time = time.time()
    tasks = Task.objects.filter(user=request.user)
    end_time = time.time()
    print(f"Task list: {end_time - start_time}")
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    start_time = time.time()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    end_time = time.time()
    print(f"Add task: {end_time - start_time}")
    return render(request, 'add_task.html', {'form': form})


def custom_logout(request):
    start_time = time.time()
    logout(request)
    end_time = time.time()
    print(f"Add task: {end_time - start_time}")
    return redirect('task_list')

@login_required
def toggle_task(request, task_id):
    start_time =time.time()
    task = get_object_or_404(Task, id=task_id,user=request.user)
    task.toggle_complete()
    end_time = time.time()
    print(f"Toggle task: {end_time - start_time}")
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    start_time = time.time()
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    end_time = time.time()
    print(f"Delete task: {end_time - start_time}")
    return redirect('task_list')