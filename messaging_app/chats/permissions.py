from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    allow only authenticated users
    allow access only if the user is a participant of the conversation.
    """
    
    SAFE_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user and request.user.is_authenticated
    

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        if request.method not in permissions.SAFE_METHODS:
            return False

        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False
