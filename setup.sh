#!/bin/bash
# Setup script for NFL Props JSON Fetcher

echo "======================================"
echo "NFL Props JSON Fetcher - Setup"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Run the script manually:"
echo "   python3 fetch_nfl_props.py"
echo ""
echo "2. Set up automatic updates (cron job):"
echo "   crontab -e"
echo "   Then add:"
echo "   0 * * * * cd $(pwd) && python3 fetch_nfl_props.py >> nfl_props.log 2>&1"
echo ""
echo "3. View example frontend:"
echo "   Open example.html in a web browser"
echo ""
echo "4. Deploy to Digital Ocean Spaces (optional):"
echo "   - Set environment variables:"
echo "     export DO_SPACE_NAME='your-space-name'"
echo "     export DO_ACCESS_KEY='your-access-key'"
echo "     export DO_SECRET_KEY='your-secret-key'"
echo "   - Install boto3: pip3 install boto3"
echo "   - Run: python3 deploy_to_spaces.py"
echo ""

