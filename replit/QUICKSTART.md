# 🚀 5-Minute Replit Setup

## Step-by-Step Visual Guide

---

### ✅ **Step 1: Create Repl** (1 minute)

1. Go to **[replit.com](https://replit.com)**
2. Click **"+ Create Repl"** button
3. Choose **"Python"** template
4. Name: `nfl-props-api`
5. Click **"Create Repl"**

---

### ✅ **Step 2: Upload Files** (2 minutes)

Upload these 4 files from the `replit` folder:

```
✓ main.py              (the main server code)
✓ requirements.txt     (dependencies)
✓ .replit              (configuration)
✓ README.md            (documentation - optional)
```

**How to upload:**
- Drag files into Replit, OR
- Click "Upload file" button, OR
- Copy/paste code directly

---

### ✅ **Step 3: Add Secret** (1 minute)

**🔒 This is the most important step!**

1. Click **🔒 Secrets** icon (lock icon in left sidebar)
2. Click **"+ New Secret"**
3. Fill in:

```
Key:   NFL_API_URL

Value: https://xml.sportsdatasolutions.com/api/v2/?reportid=nflprojections&view=passingyards&apikey=gBCLfS2nw68j38874HJrgscQtG9znGWEP4bW
```

4. Click **"Add new secret"**

**✅ This keeps your API URL completely hidden from users!**

---

### ✅ **Step 4: Run** (1 minute)

1. Click the big green **"Run"** button at top
2. Wait ~30 seconds for first-time setup
3. Watch the console - you should see:

```
✅ Success! Fetched 30 NFL player records
✅ Server is ready and running!
📍 Your API will be available at: https://...
```

---

### ✅ **Step 5: Get Your URL**

After running, Replit shows your URL at the top:

```
https://nfl-props-api.your-username.repl.co
```

**Your API endpoint is:**
```
https://nfl-props-api.your-username.repl.co/api/props
```

**✅ Copy this URL - use it in your frontend!**

---

## 🎨 Test It

### In Browser:
Visit: `https://your-repl-url.repl.co/api/props`

Should see JSON data!

### In Frontend:
```javascript
fetch('https://your-repl-url.repl.co/api/props')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## ✅ What You Get

- ✅ Automatic hourly updates
- ✅ Fast cached responses
- ✅ XML source completely hidden
- ✅ CORS enabled (works with any frontend)
- ✅ 30+ NFL player projections
- ✅ Professional API endpoints

---

## 🎯 Files Location

All files are in: `/Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON/replit/`

Or on GitHub: https://github.com/vsinaccounts/nflpropsJSON/tree/main/replit

---

## 📞 Need Help?

- **No data?** Check that you added the Secret correctly
- **Server stops?** Need Replit "Always On" ($20/mo)
- **Errors?** Check console logs for details

Read full documentation: `README.md`

---

**You're done! The XML source is hidden, data updates hourly, and your frontend can now call a clean JSON API!** 🎉

