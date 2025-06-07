"""
Custom permissions to ensure users can access their messages and coversations only
"""

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Checks if the users are part of the conversation to enable them to edit/view
    """
    def has_object_permission(self, request, view, obj):
        #if the object has user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        #if the object has sender attribute
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        #if the object has participants attribute
        if hasattr(obj, 'participants'):
            return request.participants in obj.participants.all()
        
        return False
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of the conversation to edit it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            #check if user is authenticated
            if hasattr(obj, 'user'):
                return obj.user == request.user
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                # For messages, check if user is part of the conversation
                return (hasattr(obj.conversation, 'user') and obj.conversation.user == request.user) or \
                       (hasattr(obj.conversation, 'participants') and request.user in obj.conversation.participants.all())
        
        # Write permissions only to the owner
        return self.has_object_permission(request, view, obj) if request.method in permissions.SAFE_METHODS else self._is_owner(request.user, obj)
