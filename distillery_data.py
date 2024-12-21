import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_distillery_by_slug(slug):
    """
    Fetches data for a specific distillery by its slug.
    Args:
        slug (str): The distillery identifier
    Returns:
        dict: Distillery data or None if the request fails
    """
    base_url = f"https://whiskyhunter.net/api/distillery_data/{slug}/"
    username = os.getenv('WHISKY_HUNTER_USERNAME')
    password = os.getenv('WHISKY_HUNTER_PASSWORD')

    try:
        if username and password:
            response = requests.get(base_url, auth=HTTPBasicAuth(username, password))
        else:
            response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching distillery data for {slug}: {e}")
        return None

if __name__ == "__main__":
    # Test with an example slug
    example_slug = "macallan"  # Replace with a valid distillery slug
    data = get_distillery_by_slug(example_slug)
    if data:
        print(f"Data for distillery {example_slug}:")
        print(data) 