from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete

@receiver(post_save, sender=Message, dispatch_uid="new_message")
def new_message(sender, instance, create, *kwargs):
    """Send a  when users receive a new message"""
    if create:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def logging_edits(sender, instance, *kwargs):
    """Signal to log the old message into the model MessageHistory before editing"""

    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message_id = original,
                    old_content = original.content
                )
                instance.edited = True
        
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup(sender, instance, **kwargs):
    """Deletes user data after account deletion"""
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()