from django.contrib import admin
from .models import Users
from django.contrib.auth.forms import UserChangeForm


class UserForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'company_owner', 'library_owner']
    list_display_links = ['id', 'username']
    form = UserForm


admin.site.register(Users, UserAdmin)
