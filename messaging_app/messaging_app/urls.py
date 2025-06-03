from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('chats.urls')),
]
