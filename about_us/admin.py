from django.contrib import admin

from .models import TermsOfUse, AboutUs, PrivacyPolice


class AboutUsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TermsOfUseAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PrivacyPolicyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(TermsOfUse, TermsOfUseAdmin)
admin.site.register(PrivacyPolice, PrivacyPolicyAdmin)
