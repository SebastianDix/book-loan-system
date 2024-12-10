from rest_framework.serializers import ModelSerializer

from book_loan_system.books.models import Publisher, Language, Genre, Author


class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "website", "country"]


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ["name", "iso_code"]

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "death_date",
            "bio",
        ]


class AuthorNameSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "first_name",
            "last_name",
        ]
