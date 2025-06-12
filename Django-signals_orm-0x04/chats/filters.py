from .models import Message
import django_filters


class MessageFilter(django_filters.FilterSet):
    """
    Filter for messages based on conversation ID and sender ID.
    """
    conversation_id = django_filters.NumberFilter(field_name='conversation__id', lookup_expr='exact')
    sender_id = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    sent_at = django_filters.DateTimeFromToRangeFilter(field_name='sent_at', look_up_expr='range')

    class Meta:
        model = Message
        fields = ['conversation_id', 'sender_id', 'sent_at']