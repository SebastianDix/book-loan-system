import pghistory
from django.db import models
from django.db.models import TextChoices

from book_loan_system.books.models.metadata_models import Author, Genre, Language, Publisher
from book_loan_system.contrib.models import BaseModel


# @pghistory.track()
class Book(BaseModel):
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    summary = models.TextField(blank=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="books")

    def __str__(self):
        return self.title


# @pghistory.track()
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


# @pghistory.track()
class Copy(BaseModel):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="copies")
    acquisition_date = models.DateField(auto_now_add=True)
    condition = models.CharField(max_length=50, choices=BookConditionChoices)

    def __str__(self):
        return f"Copy of {self.edition}"
