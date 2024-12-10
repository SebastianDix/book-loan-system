# Generated by Django 5.0.10 on 2024-12-10 18:23

from django.db import migrations


def create_sample_data(apps, schema_editor):
    # Get models
    Language = apps.get_model('books', 'Language')
    Genre = apps.get_model('books', 'Genre')
    Author = apps.get_model('books', 'Author')
    Book = apps.get_model('books', 'Book')
    Edition = apps.get_model('books', 'Edition')
    Copy = apps.get_model('books', 'Copy')
    Publisher = apps.get_model('books', 'Publisher')

    # Create languages
    english = Language.objects.create(name="English", iso_code="en")
    spanish = Language.objects.create(name="Spanish", iso_code="es")

    # Create genres
    classic = Genre.objects.create(name="Classic")
    drama = Genre.objects.create(name="Drama")
    fiction = Genre.objects.create(name="Fiction")

    # Create authors
    fitzgerald = Author.objects.create(first_name="F. Scott", last_name="Fitzgerald", birth_date="1896-09-24",
                                       death_date="1940-12-21")
    lee = Author.objects.create(first_name="Harper", last_name="Lee", birth_date="1926-04-28", death_date="2016-02-19")

    # Create publishers
    scribner = Publisher.objects.create(name="Scribner", website="https://scribnerbooks.com", country="United States")
    lippincott = Publisher.objects.create(name="J.B. Lippincott & Co.", website="https://lippincottbooks.com",
                                          country="United States")

    # Create books
    gatsby = Book.objects.create(title="The Great Gatsby", language=english)
    gatsby.authors.add(fitzgerald)
    gatsby.genres.add(classic, drama)

    mockingbird = Book.objects.create(title="To Kill a Mockingbird", language=english)
    mockingbird.authors.add(lee)
    mockingbird.genres.add(fiction)

    # Create editions
    gatsby_edition = Edition.objects.create(
        book=gatsby,
        publisher=scribner,
        publication_date="1925-04-10",
        isbn="9780743273565",
        page_count=180
    )

    mockingbird_edition = Edition.objects.create(
        book=mockingbird,
        publisher=lippincott,
        publication_date="1960-07-11",
        isbn="9780061120084",
        page_count=281
    )

    # Create copies
    Copy.objects.create(
        edition=gatsby_edition,
        acquisition_date="2023-01-15",
        condition="good",
    )

    Copy.objects.create(
        edition=mockingbird_edition,
        acquisition_date="2022-12-10",
        condition="new",
    )


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0002_make_models_auditable'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]