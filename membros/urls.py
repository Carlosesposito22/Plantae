from django.urls import path
from .views import UserRegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', UserRegisterView.as_view(), name='register'),
]
