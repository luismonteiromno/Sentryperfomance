from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib import messages
from .models import Books, Companys, BookGenres
from django import forms


# class BookForm(forms.ModelForm):
#
#     def clean(self):
#         cleaned_data = super().clean()
#         authors = cleaned_data.get('author')
#
#         request = self.Meta.formfield_callback.keywords['request']
#         user = request.user.email
#         print(user)
#         print(authors)
#         # if user in authors:
#         #     print('test')
#         #     self.fields['create_at'].disabled = False
#         # else:
#         #     self.fields['create_at'].disabled = True


class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state', 'in_stock']
    list_per_page = 100
    search_help_text = "Exemplo tal"
    list_filter = ['state', 'book_genre', 'publishing_company__name']
    search_fields = ['author__username']
    filter_horizontal = ['author', 'book_genre']

    fieldsets = (
        ('Informações do Livro',
         {'fields': ('title', 'price', 'author', 'release_year', 'state', 'pages', 'book_genre', 'publishing_company', 'in_stock')}),
        ('Lançamento', {'fields': ('create_at',)}),
    )

    def has_change_permission(self, request, obj=None):
        if request.user.library_owner == True or request.user.company_owner == True:
            return True
        else:
            return False

class CompanysAdmin(admin.ModelAdmin):
    search_fields = ['name', 'owner__username']
    list_display = ['id', 'name']
    filter_horizontal = ['owner']


admin.site.register(Books, BooksAdmin)
admin.site.register(Companys, CompanysAdmin)
admin.site.register(BookGenres)
