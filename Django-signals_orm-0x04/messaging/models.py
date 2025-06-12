from django.db import models
from django.contrib.auth.models import User
import uuid

class Message(models.Model):
    message_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'message_sender')
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'message_receiver')
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        if self.parent_message:
            return f"Reply from {self.sender.username}"
        return f"Message from {self.sender.username} at {self.timestamp}"
    
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

class MessageHistory(models.Model):
    histroy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by =  models.ForeignKey(Message, on_delete=models.CASCADE, related_name='edited_by', null=True, blank=True)

    def __str__(self):
        return f"Old version of message {self.original_message.message_id} at {self.edited_at}"