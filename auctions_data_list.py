import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def get_auctions_data_list():
    """
    Fetches list of all auctions from WhiskyHunter API.
    Returns:
        list: All auction data or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/auctions_data/"
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
        print(f"Error fetching auctions list: {e}")
        return None

def display_auctions(data, limit=None):
    """
    Display auction records with optional limit.
    Args:
        data: List of auction records
        limit: Number of records to show (None for all records)
    """
    if not data:
        return

    total_records = len(data)
    records_to_show = data[:limit] if limit else data
    records_shown = len(records_to_show)

    print(f"\nShowing {records_shown} of {total_records} auction records:")
    
    for i, auction in enumerate(records_to_show, 1):
        print(f"\nAuction {i}:")
        for key, value in auction.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch and display auction data from WhiskyHunter API')
    parser.add_argument('--limit', type=int, help='Number of records to display (default: all)')
    args = parser.parse_args()

    data = get_auctions_data_list()
    if data:
        display_auctions(data, limit=args.limit)
    else:
        print("Failed to fetch auction data")