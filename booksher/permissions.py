from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBookOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsTradeParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.sender == request.user or obj.getter == request.user)

class IsTradeGetter(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.getter == request.user