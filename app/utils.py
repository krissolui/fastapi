from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(plain_text: str) -> str:
    return pwd_context.hash(plain_text)


def verify(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
