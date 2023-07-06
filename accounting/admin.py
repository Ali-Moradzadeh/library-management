from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


class UserAdmin(BaseUserAdmin):
	list_display = (
		'id', 'phone_number', 'role', 'is_superuser',
		'is_staff', 'is_active', 'last_login', 'created' 
	)
	list_filter = ('role', )

	readonly_fields = ('last_login', )

	fieldsets = (
		('Main', {'fields':('phone_number', 'username', 'email', 'role', 'password')}),
		('Simple Permissions', {'fields':(
			'is_active', 'is_staff', 'is_superuser', 'last_login', 
		)}),
		('Complex Permissions', {'fields': (
		    'groups', 'user_permissions', 
		)}),
	)

	add_fieldsets = (
		('Main', {'fields':('username', 'phone_number','email', 'role', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}),
	)

	search_fields = ('username', 'phone_number', 'role')
	ordering = ('id', 'role',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.AdminProfile)
admin.site.register(models.CustomerProfile)