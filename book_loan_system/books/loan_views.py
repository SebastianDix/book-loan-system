from datetime import date

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from book_loan_system.books.models import Loan, Patron, Reservation, Fine, Copy
from book_loan_system.books.serializers.loan_serializers import LoanSerializer, PatronSerializer, FineSerializer, \
    ReservationSerializer


class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['get'], url_path='mark-returned')
    def mark_returned(self, request: Request, pk=None):
        loan = self.get_object()
        return_date = request.query_params.get('return_date', date.today())
        if isinstance(return_date, str):
            return_date = date.fromisoformat(return_date)
        if return_date > date.today():
            return Response({'error': 'Return date cannot be in the future.'}, status=status.HTTP_400_BAD_REQUEST)
        loan.status = 'returned'
        loan.return_date = return_date
        loan.save()
        return Response({'message': f'Loan {loan.id} marked as returned.'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        copy = serializer.validated_data['copy']

        # Check availability
        if Reservation.objects.filter(copy=copy, status='active').exists():
            raise ValidationError("This copy is reserved.")
        if Loan.objects.filter(copy=copy, status='on_loan').exists():
            raise ValidationError("This copy is already on loan.")

        # Get or create the Patron instance for the current user
        patron, created = Patron.objects.get_or_create(user=self.request.user)

        # Pass the patron to the serializer if not already provided
        if not serializer.validated_data.get('patron'):
            serializer.save(patron=patron)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Validate availability of the updated copy if provided
        copy = serializer.validated_data.get('copy')
        if copy and (Loan.objects.filter(copy=copy, status='on_loan').exists() or
                     Reservation.objects.filter(copy=copy, status='active').exists()):
            raise ValidationError("The selected copy is not available.")

        # Save the updated loan
        serializer.save()


class PatronViewSet(ModelViewSet):
    queryset = Patron.objects.select_related()
    serializer_class = PatronSerializer


class FineViewSet(ModelViewSet):
    queryset = Fine.objects.select_related()
    serializer_class = FineSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.select_related()
    serializer_class = ReservationSerializer
