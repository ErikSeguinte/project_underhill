from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def get_random_string():
    return secrets.token_urlsafe(5)
