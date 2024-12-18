from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_loan_system.books'

    def ready(self):
        from book_loan_system.books import signals
        assert signals
