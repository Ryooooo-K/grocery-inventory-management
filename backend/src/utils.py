import os

from azure.cosmos import CosmosClient


def get_cosmos_container_client() -> CosmosClient:
    endpoint = os.environ.get("COSMOS_ENDPOINT")
    key = os.environ.get("COSMOS_KEY")
    database_name = os.environ.get("COSMOS_DATABASE_NAME")
    container_name = os.environ.get("COSMOS_CONTAINER_NAME")

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container
