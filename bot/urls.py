from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListHistory.as_view(), name="history")
]
