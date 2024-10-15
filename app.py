import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import logging
import re
from htmlmin.main import minify
from csscompressor import compress as compress_css
from rjsmin import jsmin as compress_js
from flask_compress import Compress
from flask_minify import Minify
from scraper.scrape import tt_scrape
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

# Compress responses
Compress(app)

# Minify HTML, CSS, and JS
Minify(app=app, html=True, js=True, cssless=True)

# Enable CORS
CORS(app)

# Enable rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "5000 per hour"]  # Limit global
)

# Pretty print JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Logs
logging.basicConfig(level=logging.INFO)

# Regex
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'  # http:// or https://
    r'((?:www\.|m\.)?tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)'  # domain TikTok
    r'(:[0-9]{1,5})?'  # optional port
    r'(\/[@\w\/.-]*)?'  # TikTok path (optional)
    r'(\?[^\s]*)?$'  # optional query string
)

@app.route('/')
def index():
    # Template
    rendered_template = render_template('index.html')

    # Minify HTML
    minified_template = minify(rendered_template, remove_empty_space=True)

    # Minify inline CSS & JS
    minified_template = re.sub(
        r'<style>(.*?)<\/style>',
        lambda match: f"<style>{compress_css(match.group(1))}</style>",
        minified_template,
        flags=re.DOTALL
    )
    minified_template = re.sub(
        r'<script>(.*?)<\/script>',
        lambda match: f"<script>{compress_js(match.group(1))}</script>",
        minified_template,
        flags=re.DOTALL
    )

    return minified_template

@app.route('/download', methods=['GET'])
@limiter.limit("5000 per minute")  # Limiter
def download():
    tiktok_url = request.args.get('url')
    
    if not tiktok_url or not re.match(URL_REGEX, tiktok_url):
        logging.error('Invalid or missing URL parameter')
        return jsonify({'status': False, 'message': 'Invalid or missing URL parameter'}), 400
    
    try:
        data = tt_scrape(tiktok_url)
    except Exception as e:
        logging.error(f'Error scraping data: {e}')
        return jsonify({'status': False, 'message': 'Error scraping data'}), 500
    
    if data.get('status'):
        return jsonify(data)
    else:
        logging.warning('Failed to fetch video details')
        return jsonify({'status': False, 'message': 'Failed to fetch video details'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
