from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

#creating a router
router = routers.DefaultRouter()

#registering the viewsets
router.register(r'conversations', ConversationViewSet, basename='conversations')

#creating convo_router
convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversaton')
convo_router.register(r'messages', MessageViewSet, basename='conversation_name')

urlpatterns = [
    path('conversations', include(router.urls)),
    path('messages', include(convo_router.urls))
]