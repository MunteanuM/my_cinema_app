from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class ReservationConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, book, timestamp):
        return (
            six.text_type(book.user_id) + six.text_type(timestamp) +
            six.text_type(book.id)
        )


reservation_confirmation_token = ReservationConfirmationTokenGenerator()
