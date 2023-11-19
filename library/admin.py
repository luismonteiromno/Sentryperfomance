from django.contrib import admin
from .models import Librarys
from django import forms


class FormLibrary(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        delivery = cleaned_data.get('delivery')
        minimum_delivery = cleaned_data.get('minimum_delivery')
        maximum_delivery = cleaned_data.get('maximum_delivery')

        if delivery == True and minimum_delivery == None and maximum_delivery == None:
            raise forms.ValidationError('Preencha os campos de "tempo minímo de entrega" e "tempo máximo de entrega"!')

        if delivery == False and minimum_delivery != None and maximum_delivery != None:
            raise forms.ValidationError('Preencha o campo de "faz entrega" para que os campos '
                                        'de "tempo minímo de entrega" e "tempo máximo de entrega" sejam válidos!')

        if minimum_delivery != None and maximum_delivery != None and minimum_delivery >= maximum_delivery:
            raise forms.ValidationError('O tempo minimo de entrega não pode ser menor/igual ao tempo máximo!')


class LibraryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações da Biblioteca', {'fields': ('owner_library', 'name', 'partner_companies', 'books_for_sale')}),
        ('Localização da Biblioteca', {'fields': ('address', 'street', 'number', 'cep')}),
        ('Entrega', {'fields': ('delivery', 'minimum_delivery', 'maximum_delivery')})
    )
    form = FormLibrary
    filter_horizontal = ['partner_companies', 'books_for_sale']
    list_display = ['id', 'name']
    list_filter = ['delivery']


admin.site.register(Librarys, LibraryAdmin)
