from rest_framework import serializers
from .models import User, Conversation, Message

"""
Serializers are used to convert python objects into data types that can be rendered into JSON, XML
or other content types an vice versa
"""

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 50)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'bio', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_username(self, value):
        if "admin" in value.lower():
            raise serializers.ValidationError("User cannot contain 'admin")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
