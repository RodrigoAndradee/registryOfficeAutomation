from django.db import models
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()

    def __str__(self):
        return self.title
