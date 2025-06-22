# notion_utils/client.py
import os

from dotenv import load_dotenv
from notion_client import Client

# Load environment variables from .env file
load_dotenv()

# Debug output for checking token in development
if os.getenv("DEBUG") == "true":
    print("DEBUG NOTION_TOKEN =", os.getenv("NOTION_TOKEN"))


def get_notion_client() -> Client:
    """
    Returns a configured Notion client using the NOTION_TOKEN from environment variables.

    Raises:
        ValueError: If NOTION_TOKEN is not set in the environment.

    Returns:
        Client: An authenticated instance of the Notion API client.
    """
    # Read the API token from the environment
    token = os.getenv("NOTION_TOKEN")
    # Raise an error if the token is missing
    if not token:
        raise ValueError("NOTION_TOKEN is not set. Please check your .env file.")
    # Return the configured Notion client
    return Client(auth=token)
