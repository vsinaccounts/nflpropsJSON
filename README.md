# NFL Props JSON Fetcher

A simple Python script that fetches NFL props data from an XML API, converts it to JSON, and saves it locally. The script includes intelligent caching to only update once per hour, reducing unnecessary API calls.

## Features

- ✅ Fetches NFL props data from Sports Data Solutions API
- ✅ Automatically handles JSON data format
- ✅ Saves data to `NFLprops.json`
- ✅ Smart caching: Only updates once per hour
- ✅ Clear console output with status messages
- ✅ Error handling for network and file operations

## Installation

1. **Install Python 3.7 or higher** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install requests xmltodict
   ```

## Usage

### Run the script:

```bash
python fetch_nfl_props.py
```

Or make it executable:

```bash
chmod +x fetch_nfl_props.py
./fetch_nfl_props.py
```

### Expected Output:

**First run (or after 1 hour):**
```
============================================================
NFL Props Data Fetcher
Started at: 2025-11-14 10:30:00
============================================================
File 'NFLprops.json' does not exist. Will create new file.
Fetching data from API...
Data fetched successfully.
Converting XML to JSON...
Conversion successful.
Saving data to 'NFLprops.json'...
Data saved successfully to 'NFLprops.json'

============================================================
Update completed successfully!
============================================================
```

**Subsequent runs (within 1 hour):**
```
============================================================
NFL Props Data Fetcher
Started at: 2025-11-14 10:35:00
============================================================
File is recent (updated 0:05:00 ago). Next update in ~55 minutes.

No update needed. Exiting.
```

## Automation

### Option 1: Cron Job (Linux/Mac)

Edit your crontab:
```bash
crontab -e
```

Add this line to run every 15 minutes (script will only update if 1 hour has passed):
```
*/15 * * * * cd /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON && /usr/bin/python3 fetch_nfl_props.py >> nfl_props.log 2>&1
```

Or run every hour:
```
0 * * * * cd /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON && /usr/bin/python3 fetch_nfl_props.py >> nfl_props.log 2>&1
```

### Option 2: System Service (Linux)

Create a systemd timer for more robust scheduling.

### Option 3: Task Scheduler (Windows)

Use Windows Task Scheduler to run the script at regular intervals.

## Configuration

Edit these variables in `fetch_nfl_props.py` to customize:

```python
API_URL = "your-api-url-here"           # API endpoint
OUTPUT_FILE = "NFLprops.json"           # Output filename
UPDATE_INTERVAL_HOURS = 1               # Hours between updates
```

## Output File

The script creates `NFLprops.json` with formatted, indented JSON for easy reading and debugging. This file can be:

- Served via a web server
- Uploaded to Digital Ocean Spaces/CDN
- Used as a data source for frontend applications
- Processed by other scripts

## Deployment to Digital Ocean

### Option 1: Digital Ocean Droplet

1. Create a Droplet (Ubuntu recommended)
2. SSH into your server
3. Clone or upload this project
4. Install dependencies: `pip3 install -r requirements.txt`
5. Set up a cron job (see Automation section)
6. Serve `NFLprops.json` via Nginx or Apache

### Option 2: Digital Ocean Spaces (Static Hosting)

1. Run script locally or on a server
2. Use Digital Ocean Spaces API or web interface to upload `NFLprops.json`
3. Enable CDN for fast global access
4. Point your frontend to the Spaces URL

Example Spaces URL format:
```
https://your-space-name.nyc3.digitaloceanspaces.com/NFLprops.json
```

Or with CDN:
```
https://your-space-name.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

### Example Nginx Configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /nfl-props {
        alias /path/to/NFLPropsJSON;
        add_header Access-Control-Allow-Origin *;
        add_header Content-Type application/json;
        default_type application/json;
    }
}
```

Access via: `http://your-domain.com/nfl-props/NFLprops.json`

## Error Handling

The script handles common errors:
- Network timeouts (30 second timeout)
- API errors (HTTP status codes)
- XML parsing errors
- File write errors

Failed updates will exit with status code 1 and print error messages.

## Troubleshooting

**Permission denied error:**
```bash
chmod +x fetch_nfl_props.py
```

**Module not found error:**
```bash
pip install -r requirements.txt
```

**API timeout:**
- Check internet connection
- Verify API URL is correct
- API may be temporarily down

## License

MIT License - Free to use and modify

## Support

For issues or questions, check the script output messages for debugging information.

