from passlib.context import CryptContext

pwd_password = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_password.hash(password)

def verify(plain_password, hashed_password):
    return pwd_password.verify(plain_password,hashed_password)