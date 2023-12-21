from django.contrib import admin
from .models import BooksPurchases


# Register your models here.
class BooksPurchaseAdmin(admin.ModelAdmin):
    filter_horizontal = ['books']
    list_display = ['id', 'user']
    fields = ['user', 'books', 'type_payment', 'date']
    readonly_fields = ['date']
    date_hierarchy = 'date'


admin.site.register(BooksPurchases, BooksPurchaseAdmin)
