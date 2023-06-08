from django.contrib import admin
from core.models import Candidate,Interview,User,Category
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Interview)
admin.site.register(Category)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email','username' ,'password', 'name', 'access_control')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email','name', 'is_staff','access_control', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)


