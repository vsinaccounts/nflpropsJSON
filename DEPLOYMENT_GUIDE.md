# 🚀 Digital Ocean Deployment Guide

Complete guide for deploying your NFL Props fetcher on Digital Ocean.

---

## 📊 Deployment Options Comparison

| Method | Cost | Complexity | Best For |
|--------|------|-----------|----------|
| **GitHub Actions + Spaces** ⭐ | $5/mo | Easy | Recommended! |
| **App Platform Worker** | $5/mo | Medium | Always-on solution |
| **Droplet + Cron** | $6/mo | Easy | Full control |
| **Functions** | Pay-per-use | Medium | Sporadic usage |

---

## ⭐ Option 1: GitHub Actions + Spaces (RECOMMENDED)

**Cost:** $5/month | **Setup Time:** 10 minutes | **Maintenance:** Zero

### Why This Is Best:
- ✅ Free compute (GitHub Actions)
- ✅ Cheap storage ($5/mo for Spaces)
- ✅ Global CDN included
- ✅ No server to maintain
- ✅ Automatic updates every hour
- ✅ Version controlled

### Setup Steps:

#### 1. Create Digital Ocean Space
```bash
# Go to: https://cloud.digitalocean.com/spaces
# - Click "Create Space"
# - Name: nfl-props
# - Region: NYC3 (or your preferred region)
# - Enable CDN: ✓
# - Make it Public
```

#### 2. Get API Keys
```bash
# Go to: https://cloud.digitalocean.com/account/api/spaces
# - Click "Generate New Key"
# - Name: github-actions
# - Save the Access Key and Secret Key
```

#### 3. Add Secrets to GitHub
```bash
# Go to: https://github.com/vsinaccounts/nflpropsJSON/settings/secrets/actions
# Click "New repository secret" for each:

DO_SPACE_NAME = nfl-props
DO_SPACE_REGION = nyc3
DO_ACCESS_KEY = your-access-key-here
DO_SECRET_KEY = your-secret-key-here
```

#### 4. Enable GitHub Actions
The workflow is already in `.github/workflows/update-props.yml`

Just push it to GitHub and it will:
- Run every hour automatically
- Fetch new data
- Upload to Spaces
- Serve via CDN

#### 5. Access Your Data
```
https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

### Manual Trigger:
```bash
# Go to: https://github.com/vsinaccounts/nflpropsJSON/actions
# Select "Update NFL Props"
# Click "Run workflow"
```

---

## 🔄 Option 2: App Platform Worker

**Cost:** $5/month | **Setup Time:** 15 minutes | **Always Running:** Yes

### Run Command:
```bash
python3 worker.py
```

### Setup Steps:

#### 1. Via UI
```bash
# Go to: https://cloud.digitalocean.com/apps
# 1. Click "Create App"
# 2. Connect GitHub repo: vsinaccounts/nflpropsJSON
# 3. Select "Worker" component
# 4. Set run command: python3 worker.py
# 5. Instance: Basic XXS ($5/mo)
# 6. Deploy
```

#### 2. Via App Spec (Faster)
The configuration is in `.do/app.yaml`

```bash
# Go to: https://cloud.digitalocean.com/apps
# Click "Create App"
# Select "Import from GitHub"
# Choose: vsinaccounts/nflpropsJSON
# App Platform will auto-detect the .do/app.yaml file
```

#### 3. Add Environment Variables (Optional)
If you want to auto-upload to Spaces:

```bash
# In App Platform → Settings → Environment Variables:
DO_SPACE_NAME = nfl-props
DO_SPACE_REGION = nyc3
DO_ACCESS_KEY = your-access-key (mark as secret)
DO_SECRET_KEY = your-secret-key (mark as secret)
```

Then update `worker.py` to call `deploy_to_spaces.py` after fetching.

### How It Works:
- Worker runs continuously
- Fetches data every hour
- Logs visible in App Platform dashboard
- Auto-restarts if it crashes

### Limitations:
- Costs $5/mo even though it mostly sleeps
- JSON file stays on the worker (not accessible via URL)
- Need to combine with Spaces for public access

---

## 💻 Option 3: Droplet + Cron (Traditional)

**Cost:** $6/month | **Setup Time:** 30 minutes | **Full Control:** Yes

### Setup Steps:

#### 1. Create Droplet
```bash
# Go to: https://cloud.digitalocean.com/droplets
# - Ubuntu 22.04
# - Basic plan: $6/mo
# - Choose region
# - Add SSH key
# - Create Droplet
```

#### 2. Upload Code
```bash
# From your local machine:
scp -r /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON root@your-droplet-ip:/root/
```

#### 3. SSH and Setup
```bash
ssh root@your-droplet-ip

cd /root/NFLPropsJSON
apt update && apt install python3-pip -y
pip3 install -r requirements.txt

# Test it
python3 fetch_nfl_props.py
```

#### 4. Setup Cron Job
```bash
crontab -e

# Add this line:
0 * * * * cd /root/NFLPropsJSON && python3 fetch_nfl_props.py >> nfl_props.log 2>&1
```

#### 5. Serve with Nginx
```bash
apt install nginx -y

# Edit /etc/nginx/sites-available/default
nano /etc/nginx/sites-available/default
```

Add this location block:
```nginx
location /nfl-props.json {
    alias /root/NFLPropsJSON/NFLprops.json;
    add_header Access-Control-Allow-Origin *;
    add_header Content-Type application/json;
}
```

```bash
nginx -t
systemctl reload nginx
```

#### 6. Access Your Data
```
http://your-droplet-ip/nfl-props.json
```

---

## ⚡ Option 4: Digital Ocean Functions (Serverless)

**Cost:** $1-2/month | **Setup Time:** 20 minutes | **Serverless:** Yes

### Not Recommended Because:
- More complex setup
- Cold start delays
- Need to refactor code
- Limited execution time
- Better suited for on-demand requests

---

## 📝 Summary & Recommendations

### For Most Users: GitHub Actions + Spaces ⭐
```bash
Cost: $5/month
Compute: Free (GitHub)
Storage: Spaces with CDN
Maintenance: Zero
Scalability: Excellent
Setup: 10 minutes
```

**This is the best option because:**
- No server to maintain
- Free compute via GitHub Actions
- Global CDN distribution
- Version controlled updates
- Easy to modify schedule
- Reliable and scalable

### For Always-On Needs: App Platform Worker
```bash
Cost: $5/month
Good if: You need the worker for other tasks too
Setup: 15 minutes
```

### For Full Control: Droplet
```bash
Cost: $6/month
Good if: You want full server access
Setup: 30 minutes
```

---

## 🎯 Quick Start Commands

### GitHub Actions Setup:
```bash
# 1. Push new files to GitHub
cd /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON
git add .github/workflows/update-props.yml
git commit -m "Add GitHub Actions workflow"
git push

# 2. Add secrets on GitHub (via web UI)
# 3. Done! It will run every hour
```

### App Platform Setup:
```bash
# 1. Push worker.py to GitHub
git add worker.py .do/app.yaml
git commit -m "Add App Platform worker"
git push

# 2. Create app on Digital Ocean
# 3. Connect to GitHub repo
# 4. Deploy
```

---

## 🔍 Monitoring & Logs

### GitHub Actions:
```
https://github.com/vsinaccounts/nflpropsJSON/actions
```

### App Platform:
```
https://cloud.digitalocean.com/apps
→ Select your app
→ Runtime Logs
```

### Droplet:
```bash
ssh root@your-droplet-ip
tail -f /root/NFLPropsJSON/nfl_props.log
```

---

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| GitHub Actions | Free (2,000 min/mo) |
| DO Spaces + CDN | $5/mo |
| App Platform Worker | $5/mo |
| Droplet (Basic) | $6/mo |
| **Total (Recommended)** | **$5/mo** |

---

## ✅ Post-Deployment Checklist

- [ ] Data fetches successfully
- [ ] JSON file is accessible via URL
- [ ] Frontend can load the data
- [ ] CORS headers are set
- [ ] Automatic updates work
- [ ] Monitoring/alerts set up
- [ ] Backup plan in place

---

## 🆘 Troubleshooting

### GitHub Actions not running?
- Check secrets are set correctly
- Verify workflow file is in `.github/workflows/`
- Check Actions tab for error messages

### Can't access JSON from frontend?
- Check CORS headers
- Verify Spaces is set to Public
- Use CDN URL (faster)

### Worker keeps restarting?
- Check logs in App Platform
- Verify requirements.txt is complete
- Check for API errors

---

**Need help? Check the logs first, then review the error messages.**

