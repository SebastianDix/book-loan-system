from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from book_loan_system.books.models.loan_models import Loan
from book_loan_system.books.models.book_models import Copy, Edition
from book_loan_system.books.models.loan_models import Patron
from book_loan_system.books.models import Reservation

User = get_user_model()


class LoanViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        self.patron = Patron.objects.get(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.patron = Patron.objects.get(user=self.user)
        self.edition = Edition.objects.last()
        self.copy = Copy(
            edition=self.edition,
            acquisition_date=date.today(),
            condition='good'
        )
        self.copy.save()
        self.loan = Loan.objects.create(
            copy=self.copy,
            patron=self.patron,
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='on_loan'
        )

    def get_default_loan_data(self, copy=None) -> dict:
        data = {
            'copy': copy or self.copy.id,
            'due_date': (date.today() + timedelta(days=14)).isoformat(),
            'status': "on_loan",
            'return_date': None,
            'patron': self.patron.id,
        }
        return data

    def test_create_loan(self):
        new_copy = Copy.objects.create(
            edition=self.edition,
            acquisition_date=date.today(),
            condition='good'
        )
        data = self.get_default_loan_data(new_copy.pk)
        response = self.client.post('/api/loans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['copy'], new_copy.id)
        self.assertEqual(response.data['patron'], self.patron.id)

    def test_update_loan(self):
        new_due_date = date.today() + timedelta(days=21)
        data = {}
        data['due_date'] = new_due_date.isoformat()
        response = self.client.patch(f'/api/loans/{self.loan.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.due_date, new_due_date)

    def test_mark_returned(self):
        response = self.client.get(f'/api/loans/{self.loan.id}/mark-returned/',
                                    {'return_date': date.today().isoformat()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, 'returned')
        self.assertEqual(self.loan.return_date, date.today())

    def test_mark_returned_invalid_date(self):
        future_date = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.get(f'/api/loans/{self.loan.id}/mark-returned/', {'return_date': future_date},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('error', response.data)

    def test_create_loan_copy_already_on_loan(self):
        data = self.get_default_loan_data()
        response = self.client.post('/api/loans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This copy is already on loan.", response.data)

    def test_create_loan_copy_reserved(self):
        r = Reservation(copy=self.copy, patron=self.patron, status='active')
        r.save()

        data = self.get_default_loan_data()
        response = self.client.post('/api/loans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This copy is reserved.", response.data)
