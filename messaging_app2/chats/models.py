from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import email


class User(AbstractUser):
    """
    This model defines the user schema
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    bio = models.TextField()
    created_at = models.DateTimeField(
        default= timezone.now
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """
    This model has the conversations schema. it 
    stores the participants.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(
        default= timezone.now
    )

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """
    Model for storing messages within conversations
    Has sender, receiver, conversation and content
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    message_body = models.TextField()
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete = models.CASCADE
    )
    sender = models.ForeignKey(
        User,
        related_name='sent_message',
        on_delete = models.CASCADE
    )
    content = models.TextField()
    sent_at = models.DateTimeField(
        default= timezone.now
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"