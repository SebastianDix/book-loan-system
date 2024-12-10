from django.db import models

from book_loan_system.contrib.models import BaseModel


class Author(BaseModel):
    @property
    def repr_attributes(self):
        return "first_name", "last_name"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(BaseModel):
    @property
    def repr_attributes(self):
        return ("name",)

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("name", "country")


class Genre(BaseModel):
    @property
    def repr_attributes(self):
        return ("name",)

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Language(BaseModel):
    @property
    def repr_attributes(self):
        return "name", "iso_code"

    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
