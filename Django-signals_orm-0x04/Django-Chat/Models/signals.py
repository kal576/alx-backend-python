from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

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
