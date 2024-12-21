# Fetch general auction information from WhiskyHunter API.

# Usage:
#    python auctions_info.py   Show all records
#    python auctions_info.py --limit 5   Show first 5 records

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def get_auctions_info():
    """
    Fetches general auction information from WhiskyHunter API.
    Returns:
        list: Auction information or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/auctions_info"
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

def display_auctions_info(data, limit=None):
    """
    Display auction information with optional limit.
    Args:
        data: List of auction information
        limit: Number of records to show (None for all records)
    """
    if not data:
        return

    records_to_show = data[:limit] if limit else data
    print(f"\nShowing {'all' if limit is None else limit} of {len(data)} auction records:")
    
    for i, auction in enumerate(records_to_show, 1):
        print(f"\nAuction {i}:")
        for key, value in auction.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Fetch general auction information from WhiskyHunter API',
        epilog='''
Examples:
  python auctions_info.py          # Show all records
  python auctions_info.py --limit 5  # Show first 5 records
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--limit', type=int, help='Number of records to display (default: all)')
    args = parser.parse_args()

    data = get_auctions_info()
    if data:
        display_auctions_info(data, limit=args.limit)
    else:
        print("Failed to fetch auction information") 