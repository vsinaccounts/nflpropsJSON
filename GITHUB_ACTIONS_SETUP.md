# 🔄 GitHub Actions Setup

The GitHub Actions workflow file couldn't be pushed because your Personal Access Token needs the `workflow` scope.

## 📝 Two Ways to Add GitHub Actions:

---

### **Option 1: Add Manually via GitHub Web UI** (Easiest)

1. **Go to your repository:**
   https://github.com/vsinaccounts/nflpropsJSON

2. **Click "Add file" → "Create new file"**

3. **Name the file:**
   ```
   .github/workflows/update-props.yml
   ```

4. **Paste this content:**

```yaml
name: Update NFL Props

on:
  schedule:
    # Run every hour at the top of the hour
    - cron: '0 * * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  update-data:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install boto3
      
      - name: Fetch NFL Props data
        run: python3 fetch_nfl_props.py
      
      - name: Upload to Digital Ocean Spaces
        env:
          DO_SPACE_NAME: ${{ secrets.DO_SPACE_NAME }}
          DO_SPACE_REGION: ${{ secrets.DO_SPACE_REGION }}
          DO_ACCESS_KEY: ${{ secrets.DO_ACCESS_KEY }}
          DO_SECRET_KEY: ${{ secrets.DO_SECRET_KEY }}
        run: python3 deploy_to_spaces.py
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: nfl-props-json
          path: NFLprops.json
          retention-days: 7
```

5. **Commit the file** (click "Commit new file" button)

6. **Add GitHub Secrets:**
   - Go to: Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add these four secrets:
     - `DO_SPACE_NAME` = your-space-name
     - `DO_SPACE_REGION` = nyc3 (or your region)
     - `DO_ACCESS_KEY` = your-spaces-access-key
     - `DO_SECRET_KEY` = your-spaces-secret-key

7. **Done!** The workflow will run every hour automatically.

---

### **Option 2: Update Your PAT and Push** (For Future Updates)

If you want to push workflow files from your local machine:

1. **Generate new token with `workflow` scope:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Classic"
   - Check these scopes:
     - ✓ `repo` (Full control of private repositories)
     - ✓ `workflow` (Update GitHub Action workflows)
   - Generate and save the new token

2. **Update your remote URL:**
   ```bash
   cd /Users/danielstrauss/Desktop/CursorProjects/NFLPropsJSON
   git remote set-url origin https://NEW_TOKEN_HERE@github.com/vsinaccounts/nflpropsJSON.git
   ```

3. **Push the workflow file:**
   ```bash
   git add .github/workflows/update-props.yml
   git commit -m "Add GitHub Actions workflow"
   git push origin main
   ```

---

## ✅ Verify It's Working

1. **Go to Actions tab:**
   https://github.com/vsinaccounts/nflpropsJSON/actions

2. **You should see:** "Update NFL Props" workflow

3. **Test it manually:**
   - Click on the workflow
   - Click "Run workflow"
   - Select branch: main
   - Click "Run workflow"

4. **Check the logs** to verify it's working

---

## 🎯 What This Does

- ✅ Runs every hour (at :00 minutes)
- ✅ Fetches latest NFL props data
- ✅ Uploads to Digital Ocean Spaces
- ✅ Makes it available via CDN
- ✅ No server costs (free GitHub Actions)
- ✅ Automatic and reliable

---

## 💡 Manual Trigger

You can trigger the workflow manually anytime:

1. Go to: https://github.com/vsinaccounts/nflpropsJSON/actions
2. Select "Update NFL Props"
3. Click "Run workflow"
4. Wait ~1 minute for it to complete

---

## 📊 Usage Limits

GitHub Actions Free Tier:
- 2,000 minutes/month (free)
- Your workflow uses ~1 min/hour = 720 min/month
- **Plenty of free minutes remaining!**

---

## 🔍 Troubleshooting

### Workflow not showing up?
- Make sure file is in `.github/workflows/` directory
- File must have `.yml` or `.yaml` extension
- Refresh the Actions tab

### Workflow failing?
- Check you added all 4 secrets
- Verify secret names match exactly
- Check the workflow logs for errors

### Data not updating?
- Verify the workflow is running (check Actions tab)
- Check Digital Ocean Spaces for the file
- Verify Spaces credentials are correct

---

**Recommendation:** Use Option 1 (manual via web UI) - it's the easiest and fastest!

