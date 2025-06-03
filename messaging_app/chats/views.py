from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class  = ConversationSerializer
    permission_classes = [permissions.IsAuthenitacted]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class  = MessageSerializer
    permission_classes = [permissions.IsAuthenitacted]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
