from django.contrib import admin
from .models import Librarys


class LibraryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações da Biblioteca', {'fields': ('owner_library', 'name', 'partner_companies')}),
        ('Localização da Biblioteca', {'fields': ('address', 'street', 'number', 'cep')}),
        ('Entrega', {'fields': ('delivery', 'minimum_delivery', 'maximum_delivery')})
    )
    filter_horizontal = ['partner_companies']


admin.site.register(Librarys, LibraryAdmin)
