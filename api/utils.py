from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

def hash_password(raw_password: str) -> str:
    return make_password(raw_password)

def verify_password(stored_hash: str, raw_password: str) -> bool:
    return check_password(raw_password, stored_hash)

def create_token_pair_for_user(user_id: str, username: str) -> dict:
    refresh = RefreshToken()
    refresh["sub"] = user_id
    refresh["username"] = username
    refresh["created_at_iso"] = datetime.utcnow().isoformat()
    access = refresh.access_token
    return {"access": str(access), "refresh": str(refresh)}
