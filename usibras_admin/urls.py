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
from rest_framework import routers
from adminUsibras.views import BooksViewSet, CompanysViewSet
from library.views import LibraryViewSet

router = routers.DefaultRouter()
# from admin_notification.views import check_notification_view


def trigger_error(request):
    division_by_zero = 1 / 0


router.register(r'books', BooksViewSet, basename="Books")
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'librarys', LibraryViewSet, basename='library')

admin.site.site_title = 'API - BOOKS'
admin.site.site_header = 'BOOKS - API'
admin.site.index_title = 'BOOKS'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('check/notification', check_notification_view, name="check_notifications"),
    path('sentry-debug/', trigger_error),

]
