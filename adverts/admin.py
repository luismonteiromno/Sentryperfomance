from django.contrib import admin
from .models import Adverts, AdvertsViewed, AdvertsBooks


class AdvertsAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'library', 'create_at', 'expiration']


class AdvertsViewedAdmin(admin.ModelAdmin):
    list_display = ['user_viewed', 'announcement', 'date']


class AdvertsBooksAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'book', 'create_at', 'expiration']


admin.site.register(Adverts, AdvertsAdmin)
admin.site.register(AdvertsViewed, AdvertsViewedAdmin)
admin.site.register(AdvertsBooks, AdvertsBooksAdmin)
