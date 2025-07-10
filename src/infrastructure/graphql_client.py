# In src/infrastructure/graphql_client.py
import os
import httpx
from string import Template

# Use environment variable with fallback for local development
GRAPHQL_URL = os.environ.get("GRAPHQL_URL", "http://postgraphile:5000/graphql")


async def execute_graphql(query: str, variables: dict = None):
    """
    Execute a GraphQL query against the PostGraphile server.
    :param query: GraphQL query string to be executed.
    :param variables: Optional dictionary of variables to be substituted in the query.
    :return: JSON response from the GraphQL server.
    """
    # Use Template to substitute variables in the query string
    if variables:
        query = Template(query).safe_substitute(variables)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GRAPHQL_URL,
            json={"query": query},
        )
        return response.json()
