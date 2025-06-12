from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views import View
from .models import Message

@login_required
def delete_user(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

def conversaation_view(request):
        #get the root message(not reply)
        root_message = Message.objects.filter(parent_message__isnull=True).select_related(
                'sender', 'receiver'
        ).prefetch_related(
                'replies__sender', 'replies__receiver', 'replies__replies' 
        )

        return render(request, {'messages': root_message})

def message_thread(message):
    """Recursively build a message thread"""
    thread = {
        "message": message,
        "replies": []
    }
    for reply in message.replies.all():
        thread +=get_thread(reply)
    return thread