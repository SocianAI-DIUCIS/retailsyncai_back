# backend/api/simplejwt_auth.py
from rest_framework import exceptions
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings

# Construct TokenBackend using SIMPLE_JWT settings
# Note: TokenBackend.__init__ signature differs between versions;
# avoid passing unsupported kwargs (like `verify`) here.
token_backend = TokenBackend(
    algorithm=settings.SIMPLE_JWT.get("ALGORITHM", "HS256"),
    signing_key=settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
)

def decode_and_validate_token(token: str) -> dict:
    """
    Decode and validate a JWT using Simple JWT's TokenBackend.
    Raises rest_framework.exceptions.AuthenticationFailed on invalid/expired token.
    """
    try:
        # TokenBackend.decode will raise exceptions for invalid/expired tokens.
        payload = token_backend.decode(token, verify=True)
        return payload
    except Exception as exc:
        # Normalize to DRF authentication failure
        raise exceptions.AuthenticationFailed("Invalid or expired token") from exc
