#!/usr/bin/env python3
"""
Continuous worker for Digital Ocean App Platform
Runs the fetch script every hour in a loop
"""

import time
import subprocess
import sys
from datetime import datetime

def run_fetch_script():
    """Run the fetch script."""
    try:
        print(f"\n{'='*60}")
        print(f"Running fetch at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        result = subprocess.run(
            ['python3', 'fetch_nfl_props.py'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print("✓ Fetch completed successfully")
            
            # Optional: Upload to Digital Ocean Spaces if credentials are set
            import os
            if all([
                os.getenv('DO_SPACE_NAME'),
                os.getenv('DO_ACCESS_KEY'),
                os.getenv('DO_SECRET_KEY')
            ]):
                print("\nUploading to Digital Ocean Spaces...")
                upload_result = subprocess.run(
                    ['python3', 'deploy_to_spaces.py'],
                    capture_output=True,
                    text=True
                )
                print(upload_result.stdout)
                if upload_result.returncode == 0:
                    print("✓ Upload completed successfully")
                else:
                    print("✗ Upload failed", file=sys.stderr)
            
            return True
        else:
            print(f"✗ Fetch failed with exit code {result.returncode}", file=sys.stderr)
            return False
        
    except Exception as e:
        print(f"Error running fetch script: {e}", file=sys.stderr)
        return False


def main():
    """Main worker loop."""
    print("NFL Props Worker Started")
    print("Will fetch data every hour")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run immediately on startup
    run_fetch_script()
    
    # Then run every hour
    while True:
        print(f"\nSleeping for 1 hour... (next run at {datetime.fromtimestamp(time.time() + 3600).strftime('%H:%M:%S')})")
        time.sleep(3600)  # Sleep for 1 hour
        run_fetch_script()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Worker crashed: {e}", file=sys.stderr)
        sys.exit(1)

