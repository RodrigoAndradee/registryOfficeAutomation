from django.urls import path
from . import views

urlpatterns = [
    path('start-bot/', views.RunBot.as_view(), name="start-bot"),
]
