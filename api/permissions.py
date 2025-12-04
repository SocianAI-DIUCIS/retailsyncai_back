from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .simplejwt_auth import decode_and_validate_token

class IsAuthenticatedFromJWT(BasePermission):
    def has_permission(self, request: Request, view):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return False
        token = auth.split(" ", 1)[1]
        try:
            payload = decode_and_validate_token(token)
            request.user_payload = payload
            return True
        except Exception:
            return False
