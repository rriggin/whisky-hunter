# Fetch data for a specific distillery from WhiskyHunter API.

# Usage:
#    python distillery_data.py --list   Show available distilleries
#    python distillery_data.py macallan   Get data for specific distillery

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse
from distilleries_info import get_distilleries_info

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
    base_url = f"https://whiskyhunter.net/api/distillery_data/{slug}"
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
        # If we get a 404, suggest listing available distilleries
        if "404" in str(e):
            print(f"\nError: Distillery '{slug}' not found.")
            print("Use --list to see available distillery slugs")
        else:
            print(f"Error fetching distillery data for {slug}: {e}")
        return None

def display_available_distilleries():
    """Display list of available distillery slugs"""
    distilleries = get_distilleries_info()
    if distilleries:
        unique_distilleries = []
        seen = set()
        for distillery in distilleries:
            name = distillery['name']
            slug = distillery['slug']
            if name not in seen:
                seen.add(name)
                unique_distilleries.append((name, slug))
        
        unique_distilleries.sort()  # Sort by name
        print(f"\nAvailable distilleries ({len(unique_distilleries)}):")
        for name, slug in unique_distilleries:
            print(f"  {name} (slug: {slug})")
    else:
        print("Failed to fetch available distilleries")

def display_distillery(data):
    """
    Display detailed distillery data.
    Args:
        data: Dictionary containing distillery data
    """
    if not data:
        return

    print("\nDistillery Details:")
    for key, value in data.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch data for a specific distillery from WhiskyHunter API')
    parser.add_argument('slug', nargs='?', help='Distillery identifier (slug)')
    parser.add_argument('--list', action='store_true', help='List available distilleries')
    args = parser.parse_args()

    if args.list:
        display_available_distilleries()
    elif args.slug:
        data = get_distillery_by_slug(args.slug)
        if data:
            display_distillery(data)
        else:
            print(f"Failed to fetch data for distillery: {args.slug}")
    else:
        parser.print_help() 