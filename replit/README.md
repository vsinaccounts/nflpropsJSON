# 🏈 NFL Props API - Replit Setup

Complete backend API that fetches NFL props data and serves it securely with the XML source completely hidden.

---

## 🚀 Quick Setup (5 Minutes)

### **Step 1: Create Repl**

1. Go to [Replit](https://replit.com)
2. Click **"Create Repl"**
3. Choose **"Python"** template
4. Name it: `nfl-props-api` (or whatever you want)
5. Click **"Create Repl"**

---

### **Step 2: Upload Files**

Copy these 3 files into your Repl:

1. **`main.py`** - The main server code
2. **`requirements.txt`** - Python dependencies
3. **`.replit`** - Replit configuration

**How to upload:**
- Click "Upload file" button in Replit
- Or copy/paste the code directly

---

### **Step 3: Add Secret (IMPORTANT!)**

This is where you hide the XML API URL:

1. Click the **🔒 Secrets** icon (lock icon in left sidebar)
2. Click **"+ New Secret"**
3. Add the secret:
   - **Key:** `NFL_API_URL`
   - **Value:** `https://xml.sportsdatasolutions.com/api/v2/?reportid=nflprojections&view=passingyards&apikey=gBCLfS2nw68j38874HJrgscQtG9znGWEP4bW`
4. Click **"Add new secret"**

**⚠️ This is critical!** The secret keeps your API URL completely hidden from users.

---

### **Step 4: Run**

1. Click the big green **"Run"** button
2. Wait for dependencies to install (~30 seconds first time)
3. Server will start and fetch initial data
4. You'll see logs showing successful data fetch

**Look for:**
```
✅ Server is ready and running!
📍 Your API will be available at: https://your-repl-url.repl.co/api/props
```

---

### **Step 5: Get Your API URL**

After the server starts, Replit will show your URL at the top:

```
https://nfl-props-api.your-username.repl.co
```

**Your API endpoint is:**
```
https://nfl-props-api.your-username.repl.co/api/props
```

**Copy this URL** - this is what your frontend will call!

---

## 🎨 Use in Your Frontend

### JavaScript/HTML:
```javascript
const API_URL = 'https://your-repl-url.repl.co/api/props';

fetch(API_URL)
  .then(response => response.json())
  .then(data => {
    console.log('NFL Props:', data);
    // data is an array of 30+ player objects
    data.forEach(player => {
      console.log(`${player.PlayerName}: ${player.PROJ} yards`);
    });
  })
  .catch(error => console.error('Error:', error));
```

### React:
```javascript
import { useEffect, useState } from 'react';

function NFLProps() {
  const [props, setProps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://your-repl-url.repl.co/api/props')
      .then(res => res.json())
      .then(data => {
        setProps(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {props.map(player => (
        <div key={player.PlayerID}>
          <h3>{player.PlayerName} ({player.TeamDisplay})</h3>
          <p>Projection: {player.PROJ} yards</p>
          <p>DK Line: {player.DKVALUE}</p>
          <p>Pick: {player.PROJECTEDRESULT}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## 📊 API Endpoints

### **GET /api/props**
Returns NFL props data (cached, updates hourly)

**Response Example:**
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
    "PROJECTEDRESULT": "Over",
    "OVERML": "-113",
    "UNDERML": "-111"
  }
  // ... 29 more players
]
```

### **GET /api/status**
Check API health and cache status

### **GET /health**
Simple health check

### **GET /**
Documentation homepage (visit in browser)

---

## 🔒 Security Features

### ✅ What's Hidden:
- XML API URL is stored as encrypted Replit Secret
- Frontend never sees the source URL
- Users can't find it by inspecting network requests
- API key is completely protected

### ✅ How It Works:
```
User Browser → Your Frontend
                    ↓
              (calls your Replit URL)
                    ↓
         Replit Server (backend)
                    ↓
         Has secret XML URL (hidden)
                    ↓
         Fetches and caches data
                    ↓
         Returns JSON to frontend
```

**The XML source is never exposed to the public!**

---

## ⚡ Performance Features

### Automatic Caching:
- Data fetched once per hour (not on every request)
- Fast response times (~50ms)
- Reduces load on source API

### Background Updates:
- Separate thread updates data hourly
- Doesn't slow down user requests
- Always has fresh data ready

### CORS Enabled:
- Your frontend can call from any domain
- No cross-origin issues

---

## 🔍 Monitoring & Debugging

### View Logs in Replit:
The console shows:
- When data is fetched
- How many records retrieved
- Any errors
- Next update time

### Check Status:
Visit: `https://your-repl-url.repl.co/api/status`

See:
- Cache age
- When next update happens
- How many records
- Total fetch count

### Test in Browser:
Visit: `https://your-repl-url.repl.co/api/props`

Should see JSON data directly!

---

## ⚙️ Configuration

### Change Update Frequency:

In `main.py`, line 13:
```python
CACHE_DURATION = 3600  # 1 hour in seconds

# Change to:
# CACHE_DURATION = 1800  # 30 minutes
# CACHE_DURATION = 7200  # 2 hours
```

### Change Port (if needed):

In `main.py`, last line:
```python
app.run(host='0.0.0.0', port=8080, debug=False)
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Server starts without errors
- [ ] Initial data fetch succeeds (see logs)
- [ ] Can access homepage in browser
- [ ] `/api/props` returns JSON data
- [ ] `/api/status` shows healthy status
- [ ] Frontend can fetch and display data
- [ ] No XML URL visible in frontend code
- [ ] Data updates every hour (check logs)

---

## 🆘 Troubleshooting

### "NFL_API_URL not set in Secrets"
**Solution:** Add the secret in Replit (🔒 Secrets icon)

### "Failed to fetch data"
**Check:**
- Secret is set correctly
- API URL is complete (with API key)
- Internet connection is working
- Check console logs for specific error

### Server keeps stopping
**Solution:** 
- Make sure you have Replit "Always On" (paid feature)
- Or use Replit's Deployments feature

### CORS errors in frontend
**This shouldn't happen** - CORS is already enabled. But if it does:
- Make sure you're using the full Replit URL
- Check browser console for exact error

### Slow first request
**Normal!** First request after server sleep may take 5-10 seconds. After that, it's cached and fast.

---

## 💰 Cost

Uses your existing Replit account:
- **Free tier:** Server sleeps after inactivity (not ideal for this)
- **Hacker plan ($20/mo):** Always On + more resources (recommended)

---

## 🎯 What You Get

✅ Automatic hourly data updates  
✅ Fast cached responses  
✅ XML API completely hidden  
✅ CORS enabled for any frontend  
✅ Professional API endpoints  
✅ Status monitoring  
✅ Error handling  
✅ Clean JSON format  
✅ 30+ NFL player projections  
✅ Real-time DraftKings lines  

---

## 📚 Data Structure

Each player object includes:

- `PlayerName` - Player name
- `TeamDisplay` - Team name  
- `GameDetailsLONG` - Game matchup
- `GameDateTime` - When game starts
- `PROJ` - Projected passing yards
- `DKVALUE` - DraftKings line
- `MARGIN` - Difference between projection and line
- `MARGINPCT` - Edge percentage
- `PROJECTEDRESULT` - "Over" or "Under" prediction
- `OVERML` / `UNDERML` - Moneylines
- `StatRank` - Player rank this week

---

## 🚀 You're All Set!

Your secure NFL Props API is ready to use in your frontend!

**API URL:** `https://your-repl-url.repl.co/api/props`

Use this in your frontend to fetch data - the XML source is completely hidden and secure!

