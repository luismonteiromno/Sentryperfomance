from django.contrib import admin
from .models import Users


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'company_owner', 'library_owner']
    list_display_links = ['id', 'username']


admin.site.register(Users, UserAdmin)
