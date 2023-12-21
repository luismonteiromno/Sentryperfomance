from django.contrib import admin

from .models import Books, Companys, BookGenres


class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'state', 'in_stock']
    list_per_page = 100
    search_help_text = "Exemplo tal"
    list_filter = ['state', 'book_genre', 'publishing_company__name', 'release_year']
    search_fields = ['author__username']
    filter_horizontal = ['author', 'book_genre']
    date_hierarchy = 'create_at'

    fieldsets = (
        ('Informações do Livro',
         {'fields': ('title', 'book_cover', 'synopsis', 'price', 'author', 'release_year', 'state', 'pages', 'book_genre', 'publishing_company', 'in_stock')}),
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
