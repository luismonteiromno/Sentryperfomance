from django.contrib import admin

from .models import TermsOfUse, AboutUs


class TermsOfUseAdmin(admin.ModelAdmin):
    list_display = ['id', 'terms_of_use', 'privacy_police']


admin.site.register(AboutUs)
admin.site.register(TermsOfUse, TermsOfUseAdmin)
