from rest_framework import viewsets, permissions, status, filters
from .permissions import IsConversationParticipant
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class  = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants_username']

    def get_queryset(self):
        return Conversation.objects.filter(IsConversationParticipant)
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class  = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    order_fields = ['created_at', 'sent_at']

    def get_queryset(self):
        return Message.objects.filter(IsConversationParticipant)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    
    
