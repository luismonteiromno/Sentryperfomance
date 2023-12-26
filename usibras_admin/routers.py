from rest_framework import routers
from users.views import UsersViewSet
from adminUsibras.views import BooksViewSet, CompanysViewSet, BooksGenreViewSet
from library.views import LibraryViewSet
from purchases.views import BooksPurchasesViewSet
from about_us.views import AboutUsViewSet, TermsOfUseViewSet, PrivacyPoliceViewSet
from payment_methods.views import PaymentMethodsViewSet
from adverts.views import AdvertsViewSet, AdvertsViewedViewSet, AdvertsBooksViewSet

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename="users")
router.register(r'books', BooksViewSet, basename="Books")
router.register(r'companys', CompanysViewSet, basename='companys')
router.register(r'librarys', LibraryViewSet, basename='library')
router.register(r'books_purchase', BooksPurchasesViewSet, basename='books_purchase')
router.register(r'about_us', AboutUsViewSet, basename='about_us')
router.register(r'terms_of_use', TermsOfUseViewSet, basename='terms_of_use')
router.register(r'privacy_police', PrivacyPoliceViewSet, basename='privacy_police')
router.register(r'payment_methods', PaymentMethodsViewSet, basename='payment_methods')
router.register(r'books_genres', BooksGenreViewSet, basename='books_genres')
router.register(r'adverts', AdvertsViewSet, basename='adverts')
router.register(r'adverts_viewed', AdvertsViewedViewSet, basename='adverts_viewed')
router.register(r'adverts_books', AdvertsBooksViewSet, basename='adverts_books')
