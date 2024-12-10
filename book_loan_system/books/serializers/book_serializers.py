from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from book_loan_system.books.models import Book, Copy, Edition, Author
from book_loan_system.books.serializers.metadata_serializers import AuthorSerializer, GenreSerializer, \
    LanguageSerializer


class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'language']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'language']



class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            "book",
            "publisher",
            "publication_date",
            "isbn",
            "page_count",
        ]


class CopySerializer(ModelSerializer):
    class Meta:
        model = Copy
        fields = ["edition", "acquisition_date", "condition"]
