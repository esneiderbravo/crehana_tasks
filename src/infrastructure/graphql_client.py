import os
import httpx
from string import Template

GRAPHQL_URL = os.environ.get("GRAPHQL_URL", "http://postgraphile:5000/graphql")


async def execute_graphql(query: str, variables: dict = None):
    """
    Execute a GraphQL query against the PostGraphile server.
    :param query: GraphQL query string to be executed.
    :param variables: Optional dictionary of variables to be substituted in the query.
    :return: JSON response from the GraphQL server.
    """
    if variables:
        query = Template(query).safe_substitute(variables)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GRAPHQL_URL,
            json={"query": query},
        )
        return response.json()
