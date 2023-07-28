from django.contrib import admin
from .models import BooksPurchases


# Register your models here.
class BooksPurchaseAdmin(admin.ModelAdmin):
    filter_horizontal = ['books']
    list_display = ['user']
    fields = ['user', 'books', 'date']
    readonly_fields = ['date']


admin.site.register(BooksPurchases, BooksPurchaseAdmin)