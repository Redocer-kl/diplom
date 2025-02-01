from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, RegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически войти после регистрации
            return redirect('task_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('task_list')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.toggle_complete()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')