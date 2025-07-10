from pydantic import EmailStr

from src.application.auth import hash_password
from src.infrastructure.graphql_client import execute_graphql


async def check_existing_users_by_email(email: EmailStr):
    """
    Check if a user with the given email already exists in the database using GraphQL.
    :param email: Email address to check for existing users.
    :return: List of existing users with the given email.
    """
    check_query = """
        query GetUserByEmail {
            allUsers(condition: {email: "$email"}) {
                nodes {
                    id
                    email
                    fullName
                    password
                }
            }
        }
    """
    exists_result: dict = await execute_graphql(check_query, {"email": email})
    existing_users = exists_result.get("data", {}).get("allUsers", {}).get("nodes", [])
    return existing_users


async def create_user_graphql(user_data: dict):
    """
    Create a new user using GraphQL.
    This function hashes the password and sends a mutation to create a user.
    :param user_data: Dictionary containing user data with keys 'email', 'password', and 'full_name'.
    :return: Result of the GraphQL mutation.
    """
    password = user_data["password"]
    hashed = hash_password(password)

    create_query = """
        mutation CreateUser {
            createUser(input: {
                user: {
                    email: "$email",
                    password: "$password",
                    fullName: "$fullName"
                }
            }) {
                user {
                    id
                    email
                    fullName
                }
            }
        }
    """

    variables = {
        "email": user_data["email"],
        "password": hashed,
        "fullName": user_data["full_name"],
    }

    return await execute_graphql(create_query, variables)
