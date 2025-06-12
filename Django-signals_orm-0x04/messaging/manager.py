from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filer(receiver=user, unread=True)
    