from django.urls import path

from .views import ListChatView

urlpatterns = [
    path('', ListChatView.as_view(), name='list_chat'),
]
