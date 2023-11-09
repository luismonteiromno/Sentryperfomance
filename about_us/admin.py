from django.contrib import admin

from .models import TermsOfUse, AboutUs, PrivacyPolice


admin.site.register(AboutUs)
admin.site.register(TermsOfUse)
admin.site.register(PrivacyPolice)
