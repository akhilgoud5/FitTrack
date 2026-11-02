
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()

# JWT CONFIGURATION
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise RuntimeError("Token expiration must be positive")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from the .env file")

# PASSWORD HASHING
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot exceed 72 bytes")

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    if len(plain_password.encode("utf-8")) > 72:
        return False

    return pwd_context.verify(plain_password, hashed_password)


# JWT TOKEN GENERATION
def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
