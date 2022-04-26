from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    particpants = serializers.ListField(child=serializers.CharField())
