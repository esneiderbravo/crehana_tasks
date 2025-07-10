from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, constr
from src.controllers.users_controller import UserController

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", summary="Register a new user")
async def register_user(user: UserCreate):
    """
    Register a new user.
    :param user: UserCreate model containing email, password, and full name.
    :return: User data if registration is successful, otherwise raises HTTPException.
    """
    result = await UserController.register_user(user_data=user.model_dump())

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    if "errors" in result:
        raise HTTPException(status_code=400, detail=result["errors"])

    return result["data"]["createUser"]["user"]


@router.post("/login", summary="Login a user")
async def login_user(user: UserLogin):
    """
    Login a user with email and password.
    :param user: UserLogin model containing email and password.
    :return: Dictionary with access token and user data if login is successful, otherwise raises HTTPException.
    """
    result = await UserController.login_user(user.email, user.password)

    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])

    return result


@router.post("/invite", summary="Send an invitation to a user")
async def send_invitation(request: Request):
    """
    Send an invitation to a user by email.
    :param request: The HTTP request containing the email to which the invitation should be sent.
    :return: Success message if invitation is sent, otherwise raises HTTPException.
    """
    user_data = await request.json()
    email = user_data.get("email")
    result = await UserController.sent_invitation(email)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
