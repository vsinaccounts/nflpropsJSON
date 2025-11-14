#!/usr/bin/env python3
"""
Upload NFLprops.json to Digital Ocean Spaces
This is an optional deployment script if you want to host the JSON file on Digital Ocean Spaces.

Setup:
1. Create a Space in Digital Ocean (https://cloud.digitalocean.com/spaces)
2. Generate API keys (Spaces access key and secret key)
3. Install boto3: pip install boto3
4. Set environment variables or update the config below
"""

import os
import sys
import boto3
from botocore.exceptions import ClientError

# Configuration - Update these or use environment variables
SPACE_NAME = os.getenv('DO_SPACE_NAME', 'your-space-name')
SPACE_REGION = os.getenv('DO_SPACE_REGION', 'nyc3')  # e.g., nyc3, sfo3, sgp1
ACCESS_KEY = os.getenv('DO_ACCESS_KEY', 'your-access-key')
SECRET_KEY = os.getenv('DO_SECRET_KEY', 'your-secret-key')

# File to upload
LOCAL_FILE = 'NFLprops.json'
REMOTE_FILE = 'NFLprops.json'


def upload_to_spaces():
    """Upload the JSON file to Digital Ocean Spaces."""
    
    # Check if file exists
    if not os.path.exists(LOCAL_FILE):
        print(f"Error: {LOCAL_FILE} not found!")
        print("Run fetch_nfl_props.py first to generate the JSON file.")
        sys.exit(1)
    
    # Validate configuration
    if ACCESS_KEY == 'your-access-key' or SECRET_KEY == 'your-secret-key':
        print("Error: Please configure your Digital Ocean Spaces credentials.")
        print("Set DO_ACCESS_KEY and DO_SECRET_KEY environment variables or edit this script.")
        sys.exit(1)
    
    try:
        # Create session
        session = boto3.session.Session()
        
        # Create S3 client (Digital Ocean Spaces uses S3-compatible API)
        client = session.client(
            's3',
            region_name=SPACE_REGION,
            endpoint_url=f'https://{SPACE_REGION}.digitaloceanspaces.com',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        
        print(f"Uploading {LOCAL_FILE} to {SPACE_NAME}/{REMOTE_FILE}...")
        
        # Upload file with public-read ACL and correct content type
        client.upload_file(
            LOCAL_FILE,
            SPACE_NAME,
            REMOTE_FILE,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': 'application/json',
                'CacheControl': 'max-age=3600'  # Cache for 1 hour
            }
        )
        
        # Generate URLs
        regular_url = f"https://{SPACE_NAME}.{SPACE_REGION}.digitaloceanspaces.com/{REMOTE_FILE}"
        cdn_url = f"https://{SPACE_NAME}.{SPACE_REGION}.cdn.digitaloceanspaces.com/{REMOTE_FILE}"
        
        print("\n✅ Upload successful!")
        print(f"\nAccess URLs:")
        print(f"  Regular: {regular_url}")
        print(f"  CDN:     {cdn_url}")
        print("\n💡 Use the CDN URL for better performance and global distribution.")
        
    except ClientError as e:
        print(f"Error uploading to Spaces: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    upload_to_spaces()

