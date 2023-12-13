from django.contrib import admin
from .models import Librarys
from django import forms
from django.forms import ValidationError


class FormLibrary(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        delivery = cleaned_data.get('delivery')
        minimum_delivery = cleaned_data.get('minimum_delivery')
        maximum_delivery = cleaned_data.get('maximum_delivery')
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')

        if opening_time >= closing_time:
            raise ValidationError('O Horário de abertura não pode ser maior/igual ao horário de fechamento!')

        if delivery == True and minimum_delivery == None and maximum_delivery == None:
            raise ValidationError('Preencha os campos de "tempo minímo de entrega" e "tempo máximo de entrega"!')

        if delivery == False and minimum_delivery != None and maximum_delivery != None:
            raise ValidationError('Preencha o campo de "faz entrega" para que os campos '
                                        'de "tempo minímo de entrega" e "tempo máximo de entrega" sejam válidos!')

        if minimum_delivery != None and maximum_delivery != None and minimum_delivery >= maximum_delivery:
            raise ValidationError('O tempo minimo de entrega não pode ser maior/igual ao tempo máximo!')


class LibraryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações da Biblioteca', {'fields': ('owner_library', 'name', 'partner_companies', 'books_for_sale',
                                                  'type_payments_accepted', 'opening_time', 'closing_time')}),
        ('Localização da Biblioteca', {'fields': ('address', 'street', 'number', 'cep')}),
        ('Entrega', {'fields': ('delivery', 'minimum_delivery', 'maximum_delivery')})
    )
    form = FormLibrary
    filter_horizontal = ['owner_library', 'type_payments_accepted', 'partner_companies', 'books_for_sale']
    list_display = ['id', 'name']
    list_filter = ['delivery']


admin.site.register(Librarys, LibraryAdmin)
