# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip3 install -r requirements.txt
```

Or run the setup script:
```bash
./setup.sh
```

### Step 2: Fetch NFL Props Data
```bash
python3 fetch_nfl_props.py
```

This will create `NFLprops.json` with the latest NFL passing yards projections.

### Step 3: View the Data

**Option A: View the JSON file directly**
```bash
cat NFLprops.json
```

**Option B: Test the example frontend**
```bash
# Start a local web server
python3 -m http.server 8000

# Open in your browser:
# http://localhost:8000/example.html
```

---

## 📊 What You Get

The `NFLprops.json` file contains NFL passing yards projections with:
- Player names and teams
- Game details
- Projected passing yards
- DraftKings lines
- Over/Under predictions
- Margin analysis

Example data structure:
```json
[
  {
    "PlayerName": "Brock Purdy",
    "TeamDisplay": "49ers",
    "GameDetailsLONG": "49ers vs Cardinals",
    "PROJ": "315.966",
    "DKVALUE": "256.50",
    "MARGIN": "59.47",
    "MARGINPCT": "0.232",
    "PROJECTEDRESULT": "Over"
  }
]
```

---

## ⏰ Set Up Automatic Updates

The script only updates once per hour. To automate it:

### On Mac/Linux (cron):
```bash
crontab -e
```

Add this line to run every hour:
```
0 * * * * cd /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON && python3 fetch_nfl_props.py >> nfl_props.log 2>&1
```

### Manual runs:
Run it as many times as you want - it will only update if 1 hour has passed:
```bash
python3 fetch_nfl_props.py
```

---

## 🌐 Deploy to Digital Ocean

### Option 1: Droplet (VPS)

1. **Create a Droplet**
   - Go to [DigitalOcean](https://cloud.digitalocean.com/)
   - Create a basic Ubuntu droplet ($6/month)

2. **Upload your project**
   ```bash
   scp -r /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON root@your-droplet-ip:/root/
   ```

3. **SSH into droplet and set up**
   ```bash
   ssh root@your-droplet-ip
   cd /root/NFLPropsJSON
   ./setup.sh
   ```

4. **Set up cron job**
   ```bash
   crontab -e
   # Add: 0 * * * * cd /root/NFLPropsJSON && python3 fetch_nfl_props.py
   ```

5. **Serve with Nginx**
   ```bash
   apt install nginx
   ```

   Edit `/etc/nginx/sites-available/default`:
   ```nginx
   location /nfl-props.json {
       alias /root/NFLPropsJSON/NFLprops.json;
       add_header Access-Control-Allow-Origin *;
       add_header Content-Type application/json;
   }
   ```

   Access at: `http://your-droplet-ip/nfl-props.json`

### Option 2: Digital Ocean Spaces (CDN)

**Best for static file hosting with global CDN!**

1. **Create a Space**
   - Go to Digital Ocean → Spaces
   - Create a new Space (e.g., `nfl-props`)
   - Choose a region (e.g., NYC3)
   - Enable CDN

2. **Get API Keys**
   - Go to API → Spaces Keys
   - Generate new key pair
   - Save Access Key and Secret Key

3. **Configure and deploy**
   ```bash
   export DO_SPACE_NAME='nfl-props'
   export DO_SPACE_REGION='nyc3'
   export DO_ACCESS_KEY='your-access-key'
   export DO_SECRET_KEY='your-secret-key'
   
   pip3 install boto3
   python3 deploy_to_spaces.py
   ```

4. **Access your JSON feed**
   ```
   https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
   ```

5. **Use in your frontend**
   ```javascript
   fetch('https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json')
       .then(response => response.json())
       .then(data => console.log(data));
   ```

---

## 🎨 Frontend Integration

Update `example.html` line 116 to point to your JSON source:

```javascript
// Local file
const API_URL = './NFLprops.json';

// Your server
const API_URL = 'http://your-server.com/NFLprops.json';

// Digital Ocean Spaces CDN
const API_URL = 'https://your-space.nyc3.cdn.digitaloceanspaces.com/NFLprops.json';
```

---

## 📁 Project Files

```
NFLPropsJSON/
├── fetch_nfl_props.py      # Main script - fetches and saves data
├── deploy_to_spaces.py     # Optional - uploads to Digital Ocean Spaces
├── example.html            # Sample frontend to visualize the data
├── setup.sh                # Quick setup script
├── requirements.txt        # Python dependencies
├── README.md               # Full documentation
├── QUICKSTART.md           # This file
├── .gitignore              # Git ignore rules
└── NFLprops.json           # Generated data file (created by script)
```

---

## 🔍 Troubleshooting

**"No module named 'requests'"**
```bash
pip3 install requests
```

**"Permission denied"**
```bash
chmod +x fetch_nfl_props.py setup.sh deploy_to_spaces.py
```

**"Can't access NFLprops.json in browser"**
- Make sure you're running a web server (Python's http.server)
- Or enable CORS on your server
- Or use Digital Ocean Spaces with CDN

**Script runs but doesn't update**
- This is normal! It only updates once per hour
- Check the message: "Next update in ~X minutes"
- Delete `NFLprops.json` to force an update

---

## 💡 Pro Tips

1. **Use the CDN URL** from Digital Ocean Spaces for best performance
2. **Set up monitoring** to ensure your script keeps running
3. **Add error notifications** (email/Slack) for failed updates
4. **Cache the JSON** in your frontend for 5-15 minutes
5. **Check API limits** with your data provider

---

## 📞 Need Help?

- Check the logs: `tail -f nfl_props.log`
- Test the API: `curl "https://xml.sportsdatasolutions.com/api/v2/?reportid=nflprojections&view=passingyards&apikey=gBCLfS2nw68j38874HJrgscQtG9znGWEP4bW"`
- Verify JSON: `python3 -m json.tool NFLprops.json`

---

**Ready to go! 🏈**

