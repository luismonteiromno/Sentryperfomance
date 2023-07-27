from django.contrib import admin
from .models import Librarys


class LibraryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações da Biblioteca', {'fields': ('owner_library', 'name', 'address', 'partner_companies')}),
    )
    filter_horizontal = ['partner_companies']


admin.site.register(Librarys, LibraryAdmin)
