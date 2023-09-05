"""usibras_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from usibras_admin import settings
from rest_framework import routers
from adminUsibras.views import BooksViewSet, CompanysViewSet
from library.views import LibraryViewSet
from purchases.views import BooksPurchasesViewSet

router = routers.DefaultRouter()
# from admin_notification.views import check_notification_view


router.register(r'books', BooksViewSet, basename="Books")
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'librarys', LibraryViewSet, basename='library')
router.register(r'books_purchase', BooksPurchasesViewSet, basename='books_purchase')

admin.site.site_title = 'API - BOOKS'
admin.site.site_header = 'BOOKS - API'
admin.site.index_title = 'BOOKS'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('check/notification', check_notification_view, name="check_notifications"),
]

urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

