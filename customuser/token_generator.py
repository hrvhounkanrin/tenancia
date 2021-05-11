"""Token generator."""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """Token genrator class."""

    def _make_hash_value(self, user, timestamp):
        """Token hash."""
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = TokenGenerator()
