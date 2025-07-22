import uuid

from django.db import models

from users.models import User


# Create your models here.


class Room(models.Model):
    name = models.CharField(unique=False, null=False, blank=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name="chat_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name})"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)