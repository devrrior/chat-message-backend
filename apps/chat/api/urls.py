from django.urls import path

from .views import ChatListAPIView

urlpatterns = [
    path('', ChatListAPIView.as_view(), name='list_chat'),
]
