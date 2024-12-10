from datetime import timedelta

import pghistory
from django.conf import settings
from django.db import models
from django.db.models import TextChoices

from book_loan_system.books.models.book_models import Copy
from book_loan_system.contrib.models import BaseModel


class Patron(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patron_profile")
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

    def __repr__(self):
        """ Repr is usually used when str/printing collections, avoid n+1 query mistakes """
        return f"{self.__class__.__name__}(id={self.id}, is_active={self.is_active})"


class LoanStatusChoices(TextChoices):
    ON_LOAN = 'on_loan', 'On Loan'
    RETURNED = 'returned', 'Returned'
    OVERDUE = 'overdue', 'Overdue'


from django.utils.timezone import now
from django.conf import settings


def default_due_date():
    return now().date() + timedelta(days=getattr(settings, 'DEFAULT_LOAN_DUE_DAYS', 30))


@pghistory.track()
class Loan(BaseModel):
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name="loans")
    patron = models.ForeignKey(Patron, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=default_due_date)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('on_loan', 'On Loan'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], default='on_loan')

    def __str__(self):
        return f"Loan: {self.copy} to {self.patron.user.username}"


@pghistory.track()
class Fine(BaseModel):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine for Loan {self.loan.id}: {self.amount} {'Paid' if self.paid else 'Unpaid'}"

def default_expiration_date():
    return now().date() + timedelta(days=getattr(settings, 'DEFAULT_RESERVATION_EXPIRATION_DAYS', 30))


class Reservation(models.Model):
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name="reservations")
    patron = models.ForeignKey(Patron, on_delete=models.CASCADE, related_name="reservations")
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(default=default_expiration_date)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], default='active')

    def __str__(self):
        return f"Reservation: {self.copy} by {self.patron.user.username}"
