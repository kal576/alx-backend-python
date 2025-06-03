from django.urls import path, include
from rest_framework.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversaton')
convo_router.register(r'messages', MessageViewSet, basename='conversation_name')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls))
]