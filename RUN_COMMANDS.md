# 🚀 Run Commands for Digital Ocean App Platform

Quick reference for all deployment run commands.

---

## 📋 Summary Table

| Deployment Method | Run Command | Cost | When to Use |
|------------------|-------------|------|-------------|
| **Worker (Continuous)** | `python3 worker.py` | $5/mo | Always-on solution |
| **One-time Job** | `python3 fetch_nfl_props.py` | N/A | Manual runs only |
| **GitHub Actions** | (Automatic) | Free | Recommended! |

---

## 🔄 App Platform Worker (Continuous)

### Run Command:
```bash
python3 worker.py
```

### What It Does:
- Runs continuously
- Fetches data every hour
- Auto-uploads to Spaces (if configured)
- Restarts automatically if it crashes

### Configuration:
```yaml
# .do/app.yaml
workers:
  - name: nfl-props-worker
    run_command: python3 worker.py
    instance_size_slug: basic-xxs
```

### Setup:
1. Go to https://cloud.digitalocean.com/apps
2. Create App → Connect GitHub
3. Select: Worker component
4. Run command: `python3 worker.py`
5. Deploy

### Cost: $5/month

---

## 📝 One-Time Job (Not Recommended)

### Run Command:
```bash
python3 fetch_nfl_props.py
```

### What It Does:
- Fetches data once
- Saves to NFLprops.json
- Exits

### Why Not Recommended:
- ❌ App Platform Jobs don't have built-in scheduling
- ❌ Would need to trigger manually each time
- ❌ No automation

### Better Alternative:
Use GitHub Actions (free and automatic) or Worker (continuous).

---

## ⭐ GitHub Actions (Recommended)

### Run Command:
```
N/A - Runs automatically via GitHub Actions
```

### What It Does:
- Runs every hour automatically
- Fetches fresh data
- Uploads to Digital Ocean Spaces
- Serves via CDN globally

### Setup:
1. Add workflow file to `.github/workflows/update-props.yml`
2. Configure secrets in GitHub
3. Done! Fully automated

### Cost: FREE (uses GitHub Actions free tier)

See: `GITHUB_ACTIONS_SETUP.md` for setup instructions

---

## 🔄 Combined: Fetch + Upload

If you want to fetch AND upload in one command:

### Run Command:
```bash
python3 fetch_nfl_props.py && python3 deploy_to_spaces.py
```

### What It Does:
1. Fetches data from API
2. Saves to NFLprops.json
3. Uploads to Digital Ocean Spaces
4. Makes available via CDN

### Requirements:
- Environment variables must be set:
  - `DO_SPACE_NAME`
  - `DO_SPACE_REGION`
  - `DO_ACCESS_KEY`
  - `DO_SECRET_KEY`
- boto3 must be installed: `pip install boto3`

---

## 🎯 Quick Decision Guide

### Choose **GitHub Actions** if:
- ✅ You want it free
- ✅ You want zero maintenance
- ✅ You're okay with GitHub running it
- ✅ You want global CDN distribution

**Run Command:** (None - automatic)
**Cost:** FREE

---

### Choose **App Platform Worker** if:
- ✅ You want everything on Digital Ocean
- ✅ You need it always running
- ✅ You want DO to manage it
- ✅ You might add other tasks later

**Run Command:** `python3 worker.py`
**Cost:** $5/month

---

### Choose **Droplet + Cron** if:
- ✅ You want full control
- ✅ You're comfortable with Linux
- ✅ You need custom configuration
- ✅ You want to SSH into the server

**Run Command:** (Set up cron job)
**Cost:** $6/month

---

## 📊 Feature Comparison

| Feature | Worker | GitHub Actions | Droplet |
|---------|--------|----------------|---------|
| Run Command | `python3 worker.py` | Automatic | Cron job |
| Cost | $5/mo | Free | $6/mo |
| Setup Time | 15 min | 10 min | 30 min |
| Maintenance | Low | Zero | Medium |
| Logs | App Platform | GitHub | SSH |
| Scaling | Auto | Auto | Manual |
| CDN | Need Spaces | Included | Need setup |

---

## 🛠️ Environment Variables (for Worker)

If using App Platform Worker with auto-upload:

```bash
# Add these in App Platform → Settings → Environment Variables:

DO_SPACE_NAME = nfl-props
DO_SPACE_REGION = nyc3
DO_ACCESS_KEY = your-access-key (mark as secret)
DO_SECRET_KEY = your-secret-key (mark as secret)
```

The worker will automatically upload to Spaces after each fetch.

---

## 📝 Example App Platform Configuration

### Via UI:
```
App Type: Worker
Run Command: python3 worker.py
Build Command: pip install -r requirements.txt
Instance Size: Basic XXS ($5/mo)
Environment Variables: (add DO Spaces credentials)
```

### Via YAML (`.do/app.yaml`):
```yaml
name: nfl-props-fetcher
region: nyc
workers:
  - name: nfl-props-worker
    run_command: python3 worker.py
    instance_size_slug: basic-xxs
```

---

## ✅ Testing Locally

Before deploying, test the run commands locally:

### Test fetch:
```bash
python3 fetch_nfl_props.py
```

### Test worker:
```bash
python3 worker.py
# Press Ctrl+C to stop
```

### Test upload:
```bash
export DO_SPACE_NAME='your-space'
export DO_ACCESS_KEY='your-key'
export DO_SECRET_KEY='your-secret'
python3 deploy_to_spaces.py
```

---

## 🎉 Final Recommendation

**For Digital Ocean App Platform as a Job:**

### ⭐ Best Answer: Use Worker
```bash
Run Command: python3 worker.py
```

Why?
- App Platform doesn't have built-in cron for Jobs
- Worker runs continuously and handles scheduling
- Costs only $5/month
- Includes automatic restarts
- Easy to monitor via dashboard

### ⭐⭐ Even Better: Use GitHub Actions
```
Run Command: (automatic)
Cost: FREE
```

Why?
- No server costs
- Fully automated
- Global CDN included
- Version controlled
- Easy to modify

---

**Choose what fits your needs best!** 🚀

