from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.chat.models import Chat

from .serializers import ChatSerializer


class ListChatView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
