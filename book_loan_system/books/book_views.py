from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Book, Copy, Edition
from .serializers.book_serializers import CopySerializer, EditionSerializer, BookSerializer, BookDetailSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.prefetch_related('authors', 'genres').select_related('language')

    def get_serializer_class(self):
        return BookDetailSerializer if self.action in  ("list", "retrieve") else BookSerializer



    @action(detail=False, methods=['get'], url_path='with-available-copies')
    def with_available_copies(self, request, pk=None):
        books = Book.objects.with_available_copies()

        # Serialize and return the available copies
        serializer = BookDetailSerializer(books, many=True)
        return Response(serializer.data)



class CopyViewSet(ModelViewSet):
    queryset = Copy.objects.select_related("edition")
    serializer_class = CopySerializer

    @action(detail=False, methods=['get'], url_path='available-copies')
    def available_copies(self, request, pk=None):
        available_copies = Copy.objects.filter_available()

        # Serialize and return the available copies
        serializer = CopySerializer(available_copies, many=True)
        return Response(serializer.data)


class EditionViewSet(ModelViewSet):
    queryset = Edition.objects.select_related('book', 'publisher')
    serializer_class = EditionSerializer
