import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch


@pytest.mark.asyncio
class TestUsersRouter:

    @patch("src.controllers.users_controller.UserController.register_user")
    async def test_register_user_success(self, mock_register, test_app):
        mock_register.return_value = {
            "data": {
                "createUser": {
                    "user": {
                        "id": "123",
                        "email": "test@example.com",
                        "firstName": "Test",
                        "lastName": "User"
                    }
                }
            }
        }

        payload = {
            "email": "test@example.com",
            "password": "Password123!",
            "full_name": "Test User"
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users/register", json=payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["email"] == "test@example.com"
        assert "password" not in response.json()

    @patch("src.controllers.users_controller.UserController.register_user")
    async def test_register_user_existing_email(self, mock_register, test_app):
        mock_register.return_value = {
            "error": "Email is already registered."
        }

        payload = {
            "email": "existing@example.com",
            "password": "Password123!",
            "full_name": "Test User"
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users/register", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email is already registered" in response.text

    async def test_register_user_invalid_email(self, test_app):
        payload = {
            "email": "invalid-email",
            "password": "Password123!",
            "full_name": "Test User"
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users/register", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "email" in response.text

    @patch("src.controllers.users_controller.UserController.login_user")
    async def test_login_user_success(self, mock_login, test_app):
        mock_login.return_value = {
            "access_token": "valid.jwt.token",
            "token_type": "bearer",
            "user": {
                "id": "123",
                "email": "test@example.com",
                "full_name": "Test User"
            }
        }

        payload = {
            "email": "test@example.com",
            "password": "Password123!"
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users/login", json=payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["user"]["email"] == "test@example.com"

    @patch("src.controllers.users_controller.UserController.login_user")
    async def test_login_user_invalid_credentials(self, mock_login, test_app):
        mock_login.return_value = {
            "error": "Invalid credentials"
        }

        payload = {
            "email": "test@example.com",
            "password": "WrongPassword"
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users/login", json=payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.text