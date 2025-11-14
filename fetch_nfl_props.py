#!/usr/bin/env python3
"""
NFL Props Data Fetcher
Fetches data from API and saves to NFLprops.json
Only updates once per hour to minimize API calls.
"""

import json
import os
import time
from datetime import datetime, timedelta
import requests

# Configuration
API_URL = "https://xml.sportsdatasolutions.com/api/v2/?reportid=nflprojections&view=passingyards&apikey=gBCLfS2nw68j38874HJrgscQtG9znGWEP4bW"
OUTPUT_FILE = "NFLprops.json"
UPDATE_INTERVAL_HOURS = 1


def should_update(file_path, interval_hours=1):
    """
    Check if the file should be updated based on last modification time.
    
    Args:
        file_path: Path to the JSON file
        interval_hours: Minimum hours between updates
    
    Returns:
        True if file should be updated, False otherwise
    """
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist. Will create new file.")
        return True
    
    file_mod_time = os.path.getmtime(file_path)
    file_mod_datetime = datetime.fromtimestamp(file_mod_time)
    current_time = datetime.now()
    time_diff = current_time - file_mod_datetime
    
    if time_diff >= timedelta(hours=interval_hours):
        print(f"File is {time_diff} old. Updating...")
        return True
    else:
        time_remaining = timedelta(hours=interval_hours) - time_diff
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        print(f"File is recent (updated {time_diff} ago). Next update in ~{minutes_remaining} minutes.")
        return False


def fetch_data(url):
    """
    Fetch data from the API endpoint.
    
    Args:
        url: API endpoint URL
    
    Returns:
        Python dictionary (JSON data)
    """
    print(f"Fetching data from API...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Try to parse as JSON first
        try:
            data = response.json()
            print(f"Data fetched successfully. ({len(data)} records)")
            return data
        except json.JSONDecodeError:
            # If JSON parsing fails, return as text for potential XML parsing
            print("Data fetched successfully.")
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise


def save_json(data, file_path):
    """
    Save data as formatted JSON file.
    
    Args:
        data: Python dictionary to save
        file_path: Output file path
    """
    print(f"Saving data to '{file_path}'...")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved successfully to '{file_path}'")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        raise


def main():
    """Main execution function."""
    print("=" * 60)
    print("NFL Props Data Fetcher")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if update is needed
    if not should_update(OUTPUT_FILE, UPDATE_INTERVAL_HOURS):
        print("\nNo update needed. Exiting.")
        return
    
    try:
        # Fetch data from API
        data = fetch_data(API_URL)
        
        # Save to file
        save_json(data, OUTPUT_FILE)
        
        print("\n" + "=" * 60)
        print("Update completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nFailed to update data: {e}")
        exit(1)


if __name__ == "__main__":
    main()

