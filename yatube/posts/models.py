from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='groups',
    )
