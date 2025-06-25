from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import Post

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

admin.site.register(Post, PostAdmin)
