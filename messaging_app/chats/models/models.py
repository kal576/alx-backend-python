from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
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
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        related_name='sent_message'
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        default= timezone.now
    )
    updated_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"