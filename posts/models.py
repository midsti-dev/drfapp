from django.db import models

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


# class PostImage(models.Model):
#   image = models.ImageField

class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    caption = models.CharField(unique=False, null=False, blank=False, max_length=20, default="An image")
    file = models.FileField(upload_to="posts/files", null=False, blank=False)
    image = models.ImageField(upload_to="posts/images", null=False, blank=False)
