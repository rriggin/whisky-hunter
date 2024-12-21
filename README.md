# WhiskyHunter API Client

A Python client for interacting with the WhiskyHunter API (https://whiskyhunter.net/api/).

## Setup

bash
pip install -r requirements.txt

## Available Commands

### List All Auctions
bash
python auctions_data_list.py # Show all auctions
python auctions_data_list.py --limit 5 # Show first 5 auction

### Get Specific Auction Data
bash
python auction_data_slug.py --list        # Show available auctions
python auction_data_slug.py whiskyauctioneer  # Get data for specific auction
python auction_data_slug.py whiskyauctioneer --limit 5  # Show first 5 records

### Get Auction House Information
bash
python auctions_info.py          # Show all auction houses
python auctions_info.py --limit 5  # Show first 5 auction houses

### List All Distilleries
bash
python distilleries_info.py          # Show all distilleries
python distilleries_info.py --limit 5  # Show first 5 distilleries

### Get Specific Distillery Data
bash
python distillery_data.py --list        # Show available distilleries
python distillery_data.py macallan      # Get data for specific distillery
python distillery_data.py macallan --limit 5  # Show first 5 records


