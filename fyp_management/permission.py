from rest_framework.permissions import BasePermission
# from core.models import User

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'supervisor'

class IsFYPPanel(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'fyp_panel'

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
