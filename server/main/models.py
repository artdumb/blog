from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)


class Category(models.Model):
    category_title = models.CharField(max_length=300)


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)


class Review(models.Model):
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
