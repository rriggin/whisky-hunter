import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def get_auctions_list():
    """
    Fetches list of all auctions to find valid slugs.
    Returns:
        list: All auction data or None if the request fails
    """
    base_url = "https://whiskyhunter.net/api/auctions_data/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching auctions list: {e}")
        return None

def get_auction_by_slug(slug):
    """
    Fetches data for a specific auction by its slug.
    Args:
        slug (str): The auction identifier
    Returns:
        dict: Auction data or None if the request fails
    """
    base_url = f"https://whiskyhunter.net/api/auction_data/{slug}/"
    print(f"Trying to access: {base_url}")  # Debug line
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
        # If we get a 404, suggest listing available auctions
        if "404" in str(e):
            print(f"\nError: Auction '{slug}' not found.")
            print("Use --list to see available auction slugs")
        else:
            print(f"Error fetching auction data for {slug}: {e}")
        return None

def display_auction(data):
    """
    Display detailed auction data.
    Args:
        data: List or Dictionary containing auction data
    """
    if not data:
        return

    print("\nAuction Details:")
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"  {key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"\nRecord {i}:")
            for key, value in item.items():
                print(f"  {key}: {value}")
            print()  # Add blank line between records
    else:
        print(f"  Unexpected data type: {type(data)}")
        print(data)

def display_available_auctions():
    """Display list of available auction slugs"""
    auctions = get_auctions_list()
    if auctions:
        # Create a set of tuples containing both name and actual slug
        unique_auctions = []
        seen = set()
        for auction in auctions:
            name = auction['auction_name']
            slug = auction['auction_slug']
            if name not in seen:
                seen.add(name)
                unique_auctions.append((name, slug))
        
        unique_auctions.sort()  # Sort by name
        print(f"\nAvailable auctions ({len(unique_auctions)}):")
        for name, slug in unique_auctions:
            print(f"  {name} (slug: {slug})")
    else:
        print("Failed to fetch available auctions")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch data for a specific auction from WhiskyHunter API')
    parser.add_argument('slug', nargs='?', help='Auction identifier (slug)')
    parser.add_argument('--list', action='store_true', help='List available auctions')
    args = parser.parse_args()

    if args.list:
        display_available_auctions()
    elif args.slug:
        data = get_auction_by_slug(args.slug)
        if data:
            display_auction(data)
        else:
            print(f"Failed to fetch data for auction: {args.slug}")
    else:
        parser.print_help() 