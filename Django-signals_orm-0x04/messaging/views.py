from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views import View

@login_required
def delete_user(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
