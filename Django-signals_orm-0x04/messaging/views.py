from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views import View
from .models import Message
from django.views.decorators.cache import cache_page

@login_required
def delete_user(request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

@login_required
def send_message(request, receiver_id, parent_id=None):
    if request.method == "POST":
        content = request.POST.get("content")

         # Get the receiver and parent message if replying
        receiver = get_object_or_404(User, id=receiver_id)
        parent_message = get_object_or_404(Message, id=parent_id) if parent_id else None
        
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

        return redirect("inbox") 
    return render(request, "chat/send_message.html", {
        "receiver_id": receiver_id,
        "parent_id": parent_id
    }) 

def conversation_view(request):
        #get the root message(not reply)
        root_message = Message.objects.filter(parent_message__isnull=True).select_related(
                'sender', 'receiver'
        ).prefetch_related(
                'replies__sender', 'replies__receiver', 'replies__replies' 
        )

        def build_thread(message):
            return{
                "message": message,
                "replies": [build_thread(reply) for reply in message.replies.all()]
            }
        threads = [build_thread(msg) for msg in root_message]

        return render(request,{
              "threads": threads
        })

def unread_messages_view(request):
      unread = Message.unread.unread_for_user(request.user).only('id', 'sender', 'timestamp', 'content')

      return render(request, {
            "unread_message": unread
      })

@cache_page(60)
def cache_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender', 'receiver').only('sender', 'content', 'timestamp')
    
    return render(request, {'message': messages})