from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib import messages
from .models import Books, Companys
from django import forms


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']
        user = request.user
        # book = Books.objects.all()
        # print(book)
        # if not book.filter(author=user).exists():
        #     self.fields['create_at'].disabled = False
        # else:
        #     self.fields['create_at'].disabled = True


class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state', 'in_stock']
    list_per_page = 100
    search_help_text = "Exemplo tal"
    list_filter = ['state', 'book_genre', 'publishing_company__name']
    search_fields = ['author__username']
    filter_horizontal = ['author']
    form = BookForm

    fieldsets = (
        ('Informações do Livro',
         {'fields': ('title', 'price', 'author', 'release_year', 'state', 'pages', 'book_genre', 'publishing_company', 'in_stock')}),
        ('Lançamento', {'fields': ('create_at',)}),
    )


class CompanysAdmin(admin.ModelAdmin):
    search_fields = ['name', 'owner__username']
    list_display = ['id', 'name']
    filter_horizontal = ['owner']


admin.site.register(Books, BooksAdmin)
admin.site.register(Companys, CompanysAdmin)
