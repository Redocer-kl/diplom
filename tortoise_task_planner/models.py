from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Task(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="tasks")

    def __str__(self):
        return self.title