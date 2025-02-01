from django.db import models
from django.contrib.auth.models import User  # Используем встроенную модель User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def toggle_complete(self):
        self.is_completed = not self.is_completed
        self.save()