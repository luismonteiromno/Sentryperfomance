from django.contrib import admin
from .models import Users
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin


class UserForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class UserProfileAdmin(UserAdmin):
    fieldsets = (
        ('Informações do usuário', {'fields': ('username', 'full_name', 'is_staff', 'is_active', 'is_superuser',
                                               'groups', 'user_permissions', 'favorite_books', 'favorite_libraries',
                                               'address', 'company_owner', 'library_owner')}),
        ('Tipo do usuário', {'fields': ('type_user',)}),
        ('Contatos do usuário', {'fields': ('email', 'phone')})
    )
    list_display = ['id', 'username', 'email', 'company_owner', 'library_owner', 'type_user']
    filter_horizontal = ['user_permissions', 'favorite_books', 'favorite_libraries']
    list_display_links = ['id', 'username']
    list_filter = ['type_user', 'is_staff', 'is_superuser', 'is_active']
    form = UserForm


admin.site.register(Users, UserProfileAdmin)
