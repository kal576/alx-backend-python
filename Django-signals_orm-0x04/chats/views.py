from django.shortcuts import render
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .permissions import IsParticipantOfConversation as IsParticipant
from rest_framework.permissions import IsAuthenticated
from .pagination import customPagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    """
    ViewSet for managing conversations.
    Provides CRUD operations for conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['participants__username']
    ordering_fields = ['created_at']
  

    def get_queryset(self):
         # Don't run DB logic when generating docs
        if getattr(self, 'swagger_fake_view', False):
            return Conversation.objects.none()
        """
        Override to filter conversations by the authenticated user.
        Only conversations where the user is a participant will be returned.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of user IDs in 'participants'.
        """
        participants = request.data.get('participants', [])
        if not participants or not isinstance(participants, list):
            return Response({'error': 'Participants must be a list of user IDs.'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    """
    ViewSet for managing messages.
    Provides CRUD operations for messages within conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['sent_at']
    pagination_class = customPagination
    filterset_class = MessageFilter

    def get_queryset(self):
        # Only return messages where the request.user is a participant in the conversation
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expects 'conversation', 'sender', and 'message_body' in the request data.
        """

        conversation_id = request.data.get('conversation')

  
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({'error': 'You are not a participant in this conversation.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)