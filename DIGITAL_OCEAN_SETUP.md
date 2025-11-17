# 🚀 Digital Ocean Setup - Complete Guide

You've deployed the app! Now let's get your JSON feed URL.

---

## ✅ Your Current Setup

- ✅ App deployed on Digital Ocean App Platform
- ✅ Worker running: `python3 worker.py`
- ✅ Fetches data every hour automatically
- ⚠️ JSON file needs to be made public via Spaces

---

## 📊 Step-by-Step: Get Your JSON Feed URL

### **Step 1: Create Digital Ocean Space** (2 minutes)

1. Go to: https://cloud.digitalocean.com/spaces
2. Click **"Create Space"**
3. Fill in:
   ```
   Name: nfl-props
   Region: NYC3 (or your preferred region)
   Enable CDN: ✓ YES
   File Listing: Public
   ```
4. Click **"Create Space"**
5. **Cost:** $5/month (includes 250GB storage + CDN)

---

### **Step 2: Generate Spaces Access Keys** (1 minute)

1. Go to: https://cloud.digitalocean.com/account/api/spaces
2. Click **"Generate New Key"**
3. Name it: `github-nfl-props`
4. **SAVE BOTH KEYS:**
   - Access Key: `DO00...` (looks like this)
   - Secret Key: `xyz123...` (looks like this)
   
⚠️ **Important:** Save these now - you won't see the secret key again!

---

### **Step 3: Add Keys to Your App** (2 minutes)

1. Go to: https://cloud.digitalocean.com/apps
2. Select your app (probably called `nfl-props-fetcher`)
3. Click **"Settings"** (in the left sidebar)
4. Click **"App-Level Environment Variables"**
5. Click **"Edit"**
6. Add these 4 variables:

```
Key: DO_SPACE_NAME
Value: nfl-props
Encrypt: No

Key: DO_SPACE_REGION  
Value: nyc3
Encrypt: No

Key: DO_ACCESS_KEY
Value: [paste your Access Key]
Encrypt: Yes (✓)

Key: DO_SECRET_KEY
Value: [paste your Secret Key]
Encrypt: Yes (✓)
```

7. Click **"Save"**
8. Your app will automatically redeploy (takes 2-3 minutes)

---

### **Step 4: Wait for Upload** (Up to 1 hour)

The worker fetches data every hour, so:
- If it just ran, wait up to 1 hour
- The worker will automatically upload to Spaces on the next run
- You can check logs to see when it runs

---

### **Step 5: Get Your JSON Feed URL** ✨

Once uploaded, your JSON feed will be available at:

#### **CDN URL (Use This!)** ⭐
```
https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

#### **Direct URL**
```
https://nfl-props.nyc3.digitaloceanspaces.com/NFLprops.json
```

**Replace `nfl-props` if you named your Space differently.**

---

## 🎨 Use in Your Frontend

Update your frontend code to use the CDN URL:

```javascript
// Fetch NFL Props data
const API_URL = 'https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json';

fetch(API_URL)
  .then(response => response.json())
  .then(data => {
    console.log('NFL Props data:', data);
    // Use the data in your frontend
  })
  .catch(error => console.error('Error:', error));
```

Or in React:
```javascript
useEffect(() => {
  fetch('https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json')
    .then(res => res.json())
    .then(data => setNflProps(data));
}, []);
```

---

## 📅 About the Schedule

### ❓ Do I Need to Set a Job Scheduler?

**NO!** Your worker already has a schedule built-in.

### How It Works:

```
Worker starts → Fetches data immediately → Uploads to Spaces
     ↓
Sleeps for 1 hour
     ↓
Fetches data again → Uploads to Spaces
     ↓
Sleeps for 1 hour
     ↓
(Repeats forever)
```

### Schedule:
- **Frequency:** Every hour
- **Type:** Automatic (built into worker.py)
- **No configuration needed**

### If You Want Different Timing:

Edit the worker schedule by changing this line in `worker.py`:
```python
time.sleep(3600)  # 3600 seconds = 1 hour

# Examples:
# time.sleep(1800)  # 30 minutes
# time.sleep(7200)  # 2 hours
```

---

## 🔍 Verify It's Working

### Check App Logs:

1. Go to: https://cloud.digitalocean.com/apps
2. Select your app
3. Click **"Runtime Logs"**
4. You should see:
   ```
   Running fetch at 2025-11-14 20:00:00
   Fetching data from API...
   Data fetched successfully. (30 records)
   ✓ Fetch completed successfully
   
   Uploading to Digital Ocean Spaces...
   ✓ Upload completed successfully
   
   Sleeping for 1 hour...
   ```

### Check Spaces:

1. Go to: https://cloud.digitalocean.com/spaces
2. Click on your `nfl-props` Space
3. You should see: `NFLprops.json` file
4. Click on it to view or download

### Test the URL:

Open in browser:
```
https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

You should see the JSON data!

---

## 💰 Cost Summary

| Service | Cost | What For |
|---------|------|----------|
| **App Platform Worker** | $5/mo | Runs the fetch script |
| **Spaces + CDN** | $5/mo | Hosts JSON with global CDN |
| **Total** | **$10/mo** | Complete solution |

### 💡 Want to Save $5/month?

Use **GitHub Actions instead** (FREE):
- Stop the App Platform worker
- Set up GitHub Actions (see `GITHUB_ACTIONS_SETUP.md`)
- Still uses Spaces ($5/mo) but compute is free
- **Total cost: $5/mo**

---

## 🎯 Quick Reference

### Your JSON Feed URL:
```
https://YOUR-SPACE-NAME.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

### Updates:
- Every hour automatically
- No job scheduler needed
- Managed by the worker

### Monitoring:
- App Platform → Runtime Logs
- Spaces → Check file timestamp

---

## 🆘 Troubleshooting

### JSON not showing up in Spaces?

**Check these:**
1. ✅ Environment variables are set correctly
2. ✅ App has redeployed after adding env vars
3. ✅ Wait up to 1 hour for first upload
4. ✅ Check Runtime Logs for errors

### Can't access the JSON URL?

**Check these:**
1. ✅ Space is set to Public (not Private)
2. ✅ Using correct Space name in URL
3. ✅ File exists in Spaces
4. ✅ Using CDN URL (.cdn. in the URL)

### Worker not running?

**Check these:**
1. ✅ App is deployed and running (not paused)
2. ✅ Check Runtime Logs for errors
3. ✅ Verify requirements.txt includes boto3
4. ✅ Check app didn't crash (restart it)

### CORS errors in frontend?

Spaces automatically sets CORS headers for public files. If you still get errors:

1. Go to Spaces → Settings → CORS Configurations
2. Add:
   ```json
   {
     "AllowedOrigins": ["*"],
     "AllowedMethods": ["GET"],
     "AllowedHeaders": ["*"]
   }
   ```

---

## ✅ Final Checklist

- [ ] Digital Ocean Space created
- [ ] Spaces access keys generated
- [ ] Environment variables added to app
- [ ] App redeployed successfully
- [ ] Waited up to 1 hour for first upload
- [ ] JSON file appears in Spaces
- [ ] JSON URL accessible in browser
- [ ] Frontend can fetch the data
- [ ] CORS working correctly

---

## 🎉 You're Done!

Your setup:
- ✅ Worker fetches data every hour
- ✅ Automatically uploads to Spaces
- ✅ Available via global CDN
- ✅ JSON feed ready for frontend

**JSON Feed URL:**
```
https://nfl-props.nyc3.cdn.digitaloceanspaces.com/NFLprops.json
```

Use this URL in your frontend application!

---

## 📞 Need Help?

- Check Runtime Logs first
- Verify all environment variables
- Wait at least 1 hour after setup
- Check `NFLprops.json` exists in Spaces

**Everything should work within 1 hour of completing these steps!** 🚀

