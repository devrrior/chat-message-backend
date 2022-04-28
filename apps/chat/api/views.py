from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.chat.models import Contact

from .serializers import ChatSerializer


class ChatListAPIView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.get(user=self.request.user).chats.all()
