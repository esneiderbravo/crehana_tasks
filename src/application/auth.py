from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from functools import wraps
from fastapi import HTTPException, Request, status
from jose import jwt, JWTError

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def require_authentication(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")

        if request is None:
            raise HTTPException(status_code=400, detail="Request object is required")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            email = payload.get("sub")

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            kwargs["current_user"] = {"user_id": user_id, "email": email}

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await fn(*args, **kwargs)

    return wrapper
