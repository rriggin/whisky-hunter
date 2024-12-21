# Fetch information about all distilleries from WhiskyHunter API.

# Usage:
#    python distilleries_info.py   Show all records
#    python distilleries_info.py --limit 5   Show first 5 records

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def get_distilleries_info():
    """
    Fetches distilleries information from WhiskyHunter API.
    Returns:
        list: Distilleries information or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/distilleries_info"  # No trailing slash
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

def display_distilleries_info(data, limit=None):
    """
    Display distilleries information with optional limit.
    Args:
        data: List of distillery information
        limit: Number of records to show (None for all records)
    """
    if not data:
        return

    records_to_show = data[:limit] if limit else data
    print(f"\nShowing {'all' if limit is None else limit} of {len(data)} distillery records:")
    
    for i, distillery in enumerate(records_to_show, 1):
        print(f"\nDistillery {i}:")
        for key, value in distillery.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch distilleries information from WhiskyHunter API')
    parser.add_argument('--limit', type=int, help='Number of records to display (default: all)')
    args = parser.parse_args()

    data = get_distilleries_info()
    if data:
        display_distilleries_info(data, limit=args.limit)
    else:
        print("Failed to fetch distilleries information") 