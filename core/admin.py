from django.contrib import admin
from core.models import supervisor, department, project, milestone, fyppanel, User, notification, teamMember, University
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name', 'phoneno', 'department', 'uni', 'role', 'otp')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = ((None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'name', 'phoneno', 'department', 'uni', 'role', 'otp'),
            }),
        )


    list_display = ('email', 'name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name')

    ordering = ['id']

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_superuser and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_superuser and obj == request.user:
            return False
        return super().has_change_permission(request, obj)
        
# Register your models here.
admin.site.register(supervisor)
admin.site.register(department)
admin.site.register(project)
admin.site.register(milestone)
admin.site.register(fyppanel)
admin.site.register(User, CustomUserAdmin)
admin.site.register(notification)
admin.site.register(teamMember)
admin.site.register(University)
