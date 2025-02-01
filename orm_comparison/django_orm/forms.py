from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # Форма для регистрации

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

# Кастомная форма регистрации (если нужно добавить поля)
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']