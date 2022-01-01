from datetime import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class GenerateToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return {
            text_type(user.pk) + text_type(timestamp)
        }
generate_token = GenerateToken()        