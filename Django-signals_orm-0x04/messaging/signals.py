from .models import Message, Notification, MessageHistory
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Message, dispatch_uid="new_message")
def new_message(sender, instance, create, *kwargs):
    """Send a  when users receive a new message"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@reciever(pre_save, sender=Message)
def logging_edits(sender, instance, *kwargs):
    """Signal to log the old message into the model MessageHistory before editing"""

    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message_id = original
                    old_content = original.content
                )
                instance.edited = True
        
        except Message.DoesNotExist:
            passs
