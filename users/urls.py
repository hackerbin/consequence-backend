from django.urls import path

from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, UserAPIView

app_name = 'users'
urlpatterns = [
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/login', LoginAPIView.as_view()),
    path('auth/logout', LogoutAPIView.as_view()),
    path('auth/user', UserAPIView.as_view()),
]
