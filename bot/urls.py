from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListHistory.as_view(), name="history"),
    path('retry/<int:pk>/', views.RetryHistory.as_view(), name='retry_history')
]
