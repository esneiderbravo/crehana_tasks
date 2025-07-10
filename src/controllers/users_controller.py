from pydantic import EmailStr
from src.application.auth import verify_password, create_access_token
from src.services.user_graphql import check_existing_users_by_email, create_user_graphql


class UserController:
    @staticmethod
    async def register_user(user_data: dict):
        """
        Register a new user by checking if the email already exists and then creating the user.
        :param user_data: Dictionary containing user data with keys
        'email', 'password', and 'full_name'.
        :return: Dictionary with either an error message or the created user data.
        """
        existing_users = await check_existing_users_by_email(user_data["email"])

        if existing_users:
            return {"error": "Email is already registered."}

        return await create_user_graphql(user_data)

    @staticmethod
    async def login_user(email: EmailStr, password: str):
        """
        Login a user by checking the email and password.
        :param email: Email address of the user.
        :param password: Password of the user.
        :return: Dictionary with access token and user data if
        login is successful, otherwise an error message.
        """

        existing_users = await check_existing_users_by_email(email)

        user = next(iter(existing_users), None)
        if not user:
            return {"error": "Invalid credentials"}

        if not verify_password(password, user["password"]):
            return {"error": "Invalid credentials"}

        token = create_access_token({"sub": user["email"], "user_id": user["id"]})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["fullName"],
            },
        }

    @staticmethod
    async def sent_invitation(email: EmailStr):
        """
        Send an invitation to a user by email.
        :param email: Email address of the user to invite.
        :return: Dictionary with either an error message or a success message.
        """
        existing_users = await check_existing_users_by_email(email)

        if existing_users:
            return {"error": "Email is already registered."}

        # Here you would implement the logic to send an invitation email
        # For now, we will just return a success message
        return {"message": "Invitation sent successfully."}
