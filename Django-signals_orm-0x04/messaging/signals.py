from .models import Message, Notification
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
