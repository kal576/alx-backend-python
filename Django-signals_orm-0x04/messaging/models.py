from django.db import models
from django.contrib.auth.models import User
import uuid

class Message(models.Model):
    message_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    sender = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'message_sender')
    receiver = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'message_receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = 

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
    
class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Notification for {self.user.username} about {self.message_id}"