import os
from azure.cosmos import CosmosClient

def get_db_container(container_name):
    # Azure Cosmos DB connection details
    COSMOS_ENDPOINT = os.getenv("COMOS_ENDPOINT", "https://phnkaidb.documents.azure.com:443/")
    COSMOS_KEY = os.getenv("COSMOS_KEY", "4MLN2nFBSOodJImQX1VIfbPcxbXRPOlCCAgC28aEvUYWFr8gFWgpFtHsvj2DM8q75Kgy2RDdzR3fACDbD8a3fw==")
    
    DATABASE_NAME = "ToDoList"
    CONTAINER_NAME = container_name

    # Initialize the Cosmos client
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

    # Get the database and container
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container