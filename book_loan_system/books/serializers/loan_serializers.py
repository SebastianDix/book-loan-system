from rest_framework import serializers

from book_loan_system.books.models import Patron, Loan, Fine, Reservation, Copy


class PatronSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Patron
        fields = ['id', 'user', 'user_full_name', 'membership_date', 'is_active']


class LoanSerializer(serializers.ModelSerializer):
    copy_title = serializers.CharField(source='copy.title', read_only=True)
    patron_name = serializers.CharField(source='patron.user.get_full_name', read_only=True)
    copy = serializers.PrimaryKeyRelatedField(queryset=Copy.objects.all())  # Placeholder


    class Meta:
        model = Loan
        fields = [
            'id', 'copy', 'copy_title', 'patron', 'patron_name',
            'loan_date', 'due_date', 'return_date', 'status'
        ]


class FineSerializer(serializers.ModelSerializer):
    loan_id = serializers.PrimaryKeyRelatedField(source='loan.id', read_only=True)

    class Meta:
        model = Fine
        fields = ['id', 'loan', 'loan_id', 'amount', 'paid']


class ReservationSerializer(serializers.ModelSerializer):
    copy_title = serializers.CharField(source='copy.title', read_only=True)
    patron_name = serializers.CharField(source='patron.user.get_full_name', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'copy', 'copy_title', 'patron', 'patron_name',
            'reservation_date', 'expiration_date', 'status'
        ]
