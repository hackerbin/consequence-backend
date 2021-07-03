from django.urls import path

from core.views import PingAPIView

app_name = 'core'
urlpatterns = [
    path('ping', PingAPIView.as_view()),
]