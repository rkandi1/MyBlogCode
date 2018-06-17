from django.db import models
from django.utils import timezone


class UserAccount(models.Model):
    email = models.EmailField(max_length=30, verbose_name="email")
    password = models.CharField(max_length=50, verbose_name="password")

    def __str__(self):
        return str(self.id)


class BlogPosts(models.Model):
    title = models.CharField(max_length=100)
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="content")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
