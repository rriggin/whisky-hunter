import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_auctions_info():
    """
    Fetches list of auction information from WhiskyHunter API.
    Returns:
        list: Auction information or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/auctions_info/"
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
        print(f"Error fetching auctions info: {e}")
        return None

if __name__ == "__main__":
    data = get_auctions_info()
    if data:
        print(f"Found {len(data)} auction info records")
        print("\nFirst 3 records:")
        for info in data[:3]:
            print(info) 