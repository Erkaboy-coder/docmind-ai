from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config import settings
from jose import JWTError

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

def decode_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload

    except JWTError:
        return None