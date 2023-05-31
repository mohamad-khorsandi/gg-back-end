from rest_framework.permissions import BasePermission


class GardenOwnerPerm(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_garden_owner:
            return True
        return False
