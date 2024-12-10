from rest_framework.viewsets import ModelViewSet

from book_loan_system.books.models import Author, Language, Publisher, Genre
from book_loan_system.books.serializers.metadata_serializers import LanguageSerializer, PublisherSerializer, \
    AuthorSerializer, GenreSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
