from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from book_loan_system.books.book_views import BookViewSet, CopyViewSet, EditionViewSet
from book_loan_system.books.loan_views import LoanViewSet, PatronViewSet
from book_loan_system.books.metadata_views import AuthorViewSet, LanguageViewSet, PublisherViewSet, GenreViewSet
from book_loan_system.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("publishers", PublisherViewSet)
router.register("languages", LanguageViewSet)
router.register("copies", CopyViewSet)
router.register("editions", EditionViewSet)
router.register("genres", GenreViewSet)
router.register("loans", LoanViewSet)
router.register("patrons", PatronViewSet)



app_name = "api"
urlpatterns = router.urls
