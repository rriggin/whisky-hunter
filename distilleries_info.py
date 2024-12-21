import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_distilleries_info():
    """
    Fetches list of distillery information from WhiskyHunter API.
    Returns:
        list: Distillery information or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/distilleries_info/"
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
        print(f"Error fetching distilleries info: {e}")
        return None

if __name__ == "__main__":
    data = get_distilleries_info()
    if data:
        print(f"Found {len(data)} distillery records")
        print("\nFirst 3 records:")
        for distillery in data[:3]:
            print(distillery) 