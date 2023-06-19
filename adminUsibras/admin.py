from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib import messages
from .models import Books, Companys


class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state']
    list_per_page = 100
    search_help_text = "Exemplo tal"
    list_filter = ['state', 'book_genre', 'publishing_company__name']
    search_fields = ['author__username']
    readonly_fields = ['create_at']
    filter_horizontal = ['author']

    @staticmethod
    def detail(request):
        message = messages.success(request, f"Novo livro criado", )
        print("DEPOIS DA MENSAGEM")
        return TemplateResponse(request, 'index.html', {'message': message})


class CompanysAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name']
    filter_horizontal = ['owner']


admin.site.register(Books, BooksAdmin)
admin.site.register(Companys, CompanysAdmin)
