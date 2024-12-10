import pghistory
from django.db import models
from django.db.models import TextChoices, QuerySet, Manager, OuterRef, Exists

from book_loan_system.books.models.metadata_models import Author, Genre, Language, Publisher
from book_loan_system.contrib.models import BaseModel

from django.db import models
from django.db.models import Q


class BookQuerySet(models.QuerySet):
    def with_available_copies(self):
        # Define subquery to check if any related copies are available
        available_copies_subquery = Copy.objects.filter_available().filter(
            edition__book=OuterRef('pk'),  # Relates the subquery to the current book
        ).values('pk')  # Only need the PK to confirm existence

        # Use Exists to filter books with available copies
        return self.filter(Exists(available_copies_subquery))


@pghistory.track()
class Book(BaseModel):
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    summary = models.TextField(blank=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="books")
    objects = Manager.from_queryset(BookQuerySet)()

    def __str__(self):
        return self.title


@pghistory.track()
class Edition(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="editions")
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="editions")
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, blank=True)
    page_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book.title} ({self.publication_date})"


class BookConditionChoices(TextChoices):
    NEW = ('new', 'New')
    GOOD = ('good', 'Good')
    WORN = ('worn', 'Worn')
    DAMAGED = ('damaged', 'Damaged')


class CopyQueryset(QuerySet):
    def filter_available(self):
        return self.filter(
            ~Q(loans__status='on_loan'),
            ~Q(reservations__status='active')
        ).distinct()

    def filter_available_by_book(self, book_id: int):
        return self.filter_available().filter(edition__book=book_id)


@pghistory.track()
class Copy(BaseModel):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="copies")
    acquisition_date = models.DateField(auto_now_add=True)
    condition = models.CharField(max_length=50, choices=BookConditionChoices)
    objects = Manager.from_queryset(CopyQueryset)()

    def __str__(self):
        return f"Copy of {self.edition} in {self.condition} condition"
