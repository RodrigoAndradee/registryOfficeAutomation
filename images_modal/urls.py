from django.urls import path
from . import views

urlpatterns = [
    path("book-1/", views.FirstBook.as_view(), name="book_1"),
    path("book-2/", views.SecondBook.as_view(), name="book_2"),
]
