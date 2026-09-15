import os
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt.

    Args:
        password: Plaintext password to hash.

    Returns:
        The bcrypt hash, as a string.

    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a bcrypt hash.

    Args:
        plain_password: Plaintext password to check.
        hashed_password: Bcrypt hash to check against.

    Returns:
        True if the password matches the hash, False otherwise.

    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload data; must contain an "auth_id" key, used as the token subject.

    Returns:
        The encoded JWT.

    """
    secret_key = os.getenv("JWT_SECRET_KEY")
    algo = os.getenv("JWT_ALGORITHM")
    expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    now = datetime.now(UTC)

    payload = {
        "sub": str(data["auth_id"]),
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }

    return jwt.encode(payload, secret_key, algorithm=algo)


def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token.

    Args:
        token: Encoded JWT to decode.

    Returns:
        The decoded token payload.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is malformed or has an invalid signature.

    """
    secret_key = os.getenv("JWT_SECRET_KEY")
    algo = os.getenv("JWT_ALGORITHM")

    return jwt.decode(token, secret_key, algorithms=[algo])
