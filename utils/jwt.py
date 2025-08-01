import jwt
from datetime import datetime, timedelta
from typing import Any, Dict
from core.settings import JWT_SETTINGS


def generate_jwt(payload: Dict[str, Any], secret: str, expires_delta: timedelta) -> str:
    data = payload.copy()
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})
    token = jwt.encode(data, secret, algorithm="HS256")
    return token


def full_jwt(payload: Dict[str, Any]) -> Dict[str, str]:
    """Generate both access and refresh tokens."""
    access = generate_jwt(
        payload,
        JWT_SETTINGS["secret_key"],
        timedelta(minutes=JWT_SETTINGS["access_exp_minutes"]),
    )
    refresh = generate_jwt(
        payload,
        JWT_SETTINGS["secret_key"],
        timedelta(days=JWT_SETTINGS["refresh_exp_days"]),
    )
    return {"access_token": access, "refresh_token": refresh}


def verify_access(token: str) -> Dict[str, Any]:
    """Verify access token."""
    try:
        decoded = jwt.decode(token, JWT_SETTINGS["secret_key"], algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Access token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """Decode JWT token without verification."""
    try:
        decoded = jwt.decode(
            token, algorithms=["HS256"], key=JWT_SETTINGS["secret_key"]
        )
        return decoded
    except jwt.DecodeError:
        raise Exception("Invalid JWT token")
    except Exception as e:
        raise Exception(f"Error decoding JWT token: {str(e)}")