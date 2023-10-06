
import asyncio
import bcrypt
from app.JWTHandler import JwtHandler
from app.config import settings

jwtHandler = JwtHandler(
    access_secret_key=settings.ACCESS_SECRET_KEY,
    refresh_secret_key=settings.REFRESH_SECRET_KEY
)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def check_password(hash_password : str, checking_password: str):
    password_hash = hash_password.encode('utf-8')
    res = bcrypt.checkpw(checking_password.encode('utf-8'), password_hash)
    return res
