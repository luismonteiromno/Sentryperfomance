from rest_framework import routers
from adminUsibras.views import BooksViewSet, CompanysViewSet
from library.views import LibraryViewSet
from purchases.views import BooksPurchasesViewSet
from about_us.views import AboutUsViewSet, TermsOfUseViewSet

router = routers.DefaultRouter()

router.register(r'books', BooksViewSet, basename="Books")
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'librarys', LibraryViewSet, basename='library')
router.register(r'books_purchase', BooksPurchasesViewSet, basename='books_purchase')
router.register(r'about_us', AboutUsViewSet, basename='books_purchase')
router.register(r'terms_of_use', TermsOfUseViewSet, basename='books_purchase')
