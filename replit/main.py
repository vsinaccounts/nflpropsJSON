from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta
import threading
import time
import json

app = Flask(__name__)

# In-memory cache for NFL props data
cache = {
    'data': None,
    'last_updated': None,
    'fetch_count': 0
}

CACHE_DURATION = 3600  # 1 hour in seconds

def fetch_nfl_data():
    """
    Fetch NFL props data from XML API
    API URL is stored as Replit Secret (completely hidden)
    """
    api_url = os.environ.get('NFL_API_URL')
    
    if not api_url:
        print("❌ ERROR: NFL_API_URL not set in Replit Secrets")
        print("   Go to Secrets (🔒) and add: NFL_API_URL")
        return None
    
    try:
        print(f"\n{'='*60}")
        print(f"🔄 Fetching NFL Props Data...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Fetch data from the hidden XML API
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        # Parse JSON (API returns JSON not XML despite the domain name)
        data = response.json()
        
        # Update cache
        cache['data'] = data
        cache['last_updated'] = datetime.now()
        cache['fetch_count'] += 1
        
        print(f"✅ Success! Fetched {len(data)} NFL player records")
        print(f"📊 Total fetches since server start: {cache['fetch_count']}")
        print(f"{'='*60}\n")
        
        return data
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out - API took too long to respond")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

def is_cache_valid():
    """Check if cached data is still fresh (less than 1 hour old)"""
    if cache['data'] is None or cache['last_updated'] is None:
        return False
    
    age = datetime.now() - cache['last_updated']
    return age.total_seconds() < CACHE_DURATION

def background_updater():
    """
    Background thread that fetches fresh data every hour
    Runs independently of user requests
    """
    print("\n🚀 Background updater thread started")
    print("📅 Will fetch data every hour automatically\n")
    
    while True:
        print("\n⏰ Scheduled hourly update triggered")
        fetch_nfl_data()
        
        # Calculate next update time
        next_update = datetime.now() + timedelta(hours=1)
        print(f"😴 Sleeping for 1 hour...")
        print(f"⏭️  Next update at: {next_update.strftime('%I:%M %p')}\n")
        
        time.sleep(3600)  # Sleep for 1 hour

# ============= API ROUTES =============

@app.route('/')
def index():
    """Landing page with API documentation"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NFL Props API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            .card { 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                margin-bottom: 20px;
            }
            h1 { 
                color: #333; 
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .status { 
                color: #28a745; 
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            h2 { 
                color: #555; 
                margin-top: 30px;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .endpoint { 
                background: #f8f9fa; 
                padding: 20px; 
                border-left: 4px solid #667eea;
                margin: 15px 0;
                border-radius: 5px;
            }
            .endpoint strong {
                color: #667eea;
                font-size: 1.1em;
                display: block;
                margin-bottom: 8px;
            }
            code { 
                background: #2d2d2d; 
                color: #f8f8f2;
                padding: 15px; 
                border-radius: 5px;
                display: block;
                overflow-x: auto;
                font-size: 14px;
                line-height: 1.6;
                margin: 15px 0;
            }
            ul {
                margin-left: 20px;
                line-height: 2;
            }
            li { margin: 8px 0; }
            .feature { color: #28a745; }
            .url-box {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
                word-break: break-all;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>🏈 NFL Props API</h1>
                <p class="status">✅ API is running and healthy</p>
                
                <h2>📍 Endpoints</h2>
                
                <div class="endpoint">
                    <strong>GET /api/props</strong>
                    Returns NFL passing yards projections in JSON format.<br>
                    Data is cached and updates automatically every hour.
                </div>
                
                <div class="endpoint">
                    <strong>GET /api/status</strong>
                    Returns API health status and cache information.
                </div>
                
                <div class="endpoint">
                    <strong>GET /health</strong>
                    Simple health check endpoint.
                </div>
                
                <h2>💻 Frontend Integration</h2>
                <p>Use this in your frontend to fetch NFL props data:</p>
                <code>fetch(window.location.origin + '/api/props')
  .then(response => response.json())
  .then(data => {
    console.log('NFL Props:', data);
    // Use data in your app
  })
  .catch(error => console.error('Error:', error));</code>
                
                <h2>🔧 Features</h2>
                <ul>
                    <li class="feature">✅ Automatic hourly data updates</li>
                    <li class="feature">✅ Fast cached responses (1 hour cache)</li>
                    <li class="feature">✅ CORS enabled for frontend access</li>
                    <li class="feature">✅ Source API URL completely hidden</li>
                    <li class="feature">✅ 30+ NFL player projections</li>
                    <li class="feature">✅ Real-time DraftKings lines</li>
                </ul>
                
                <h2>📊 Data Format</h2>
                <p>Each player record includes:</p>
                <ul>
                    <li>Player name, team, and game details</li>
                    <li>Projected passing yards (PROJ)</li>
                    <li>DraftKings line (DKVALUE)</li>
                    <li>Over/Under prediction</li>
                    <li>Margin and confidence percentage</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/api/props')
def get_props():
    """
    Main API endpoint - returns NFL props data
    This is what your frontend will call
    """
    
    # Check if cache needs refresh
    if not is_cache_valid():
        print("⚠️ Cache expired or empty, fetching fresh data...")
        fetch_nfl_data()
    
    # If still no data after fetch attempt, return error
    if cache['data'] is None:
        return jsonify({
            'error': 'Failed to fetch data',
            'message': 'Unable to retrieve NFL props data. Please try again later.',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    # Return cached data with headers
    response = jsonify(cache['data'])
    
    # CORS header - allows any website to call this API
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    # Cache control - tells browsers to cache for 1 hour
    response.headers['Cache-Control'] = 'public, max-age=3600'
    
    # Custom header showing cache age
    cache_age_seconds = int((datetime.now() - cache['last_updated']).total_seconds())
    response.headers['X-Cache-Age'] = str(cache_age_seconds)
    response.headers['X-Record-Count'] = str(len(cache['data']))
    
    return response

@app.route('/api/status')
def status():
    """
    Status endpoint - shows API health and cache information
    Useful for debugging and monitoring
    """
    if cache['last_updated']:
        age_seconds = int((datetime.now() - cache['last_updated']).total_seconds())
        next_update = cache['last_updated'] + timedelta(seconds=CACHE_DURATION)
        seconds_until_update = int((next_update - datetime.now()).total_seconds())
        
        return jsonify({
            'status': 'healthy',
            'server_time': datetime.now().isoformat(),
            'cache': {
                'is_valid': is_cache_valid(),
                'last_updated': cache['last_updated'].isoformat(),
                'age_seconds': age_seconds,
                'age_minutes': round(age_seconds / 60, 1),
                'next_update_in_seconds': max(0, seconds_until_update),
                'next_update_in_minutes': max(0, round(seconds_until_update / 60, 1)),
                'next_update_at': next_update.strftime('%I:%M %p')
            },
            'data': {
                'records': len(cache['data']) if cache['data'] else 0,
                'total_fetches': cache['fetch_count']
            },
            'api': {
                'version': '1.0',
                'endpoints': ['/api/props', '/api/status', '/health']
            }
        })
    
    return jsonify({
        'status': 'starting',
        'message': 'Server is initializing, waiting for first data fetch',
        'cache': {'is_valid': False}
    })

@app.route('/health')
def health():
    """Simple health check for monitoring"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

# Handle CORS preflight requests
@app.route('/api/props', methods=['OPTIONS'])
def handle_options():
    response = jsonify({'status': 'ok'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# ============= SERVER STARTUP =============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏈 NFL Props API Server Starting...")
    print("="*60 + "\n")
    
    # Check if API URL is configured
    if not os.environ.get('NFL_API_URL'):
        print("⚠️  WARNING: NFL_API_URL not found in Secrets!")
        print("   Please add it in Replit Secrets (🔒 icon)\n")
    
    # Start background updater thread (daemon=True means it stops when main program stops)
    print("🔧 Starting background data updater...")
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()
    
    # Fetch initial data immediately
    print("📥 Fetching initial data...\n")
    fetch_nfl_data()
    
    print("\n✅ Server is ready and running!")
    print("📍 Your API will be available at: https://your-repl-url.repl.co/api/props")
    print("📊 Visit homepage for documentation and testing\n")
    print("="*60 + "\n")
    
    # Run Flask server
    # host='0.0.0.0' makes it accessible from outside Replit
    # port=8080 is Replit's default port
    # debug=False for production (no auto-reload)
    app.run(host='0.0.0.0', port=8080, debug=False)

