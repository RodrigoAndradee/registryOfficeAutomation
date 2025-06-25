from django.urls import path
from . import views

urlpatterns = [
    path("edit-file/", views.FileEditor.as_view(), name="edit_file"),
]
