from flask import Flask, request, jsonify, render_template
import requests
import logging
import re
from htmlmin.main import minify
from csscompressor import compress as compress_css
from rjsmin import jsmin as compress_js

app = Flask(__name__)

# Logs
logging.basicConfig(level=logging.INFO)


# Regex
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'  # http:// _+ https://
    r'((([A-Za-z]{1,3})+\.)+([A-Za-z]{2,6})|'
    r'(([0-9]{1,3}\.){3}[0-9]{1,3}))'
    r'(:[0-9]{1,5})?'
    r'(\/.*)?$'
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
def download():
    tiktok_url = request.args.get('url')
    
    if not tiktok_url or not re.match(URL_REGEX, tiktok_url):
        logging.error('Invalid or missing URL parameter')
        return jsonify({'status': False, 'message': 'Invalid or missing URL parameter'}), 400
    
    api_url = f'https://widipe.com/download/ttdl?url={tiktok_url}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'Error contacting API: {e}')
        return jsonify({'status': False, 'message': 'Error contacting API'}), 500
    
    data = response.json()
    
    if data.get('status'):
        return jsonify(data['result'])
    else:
        logging.warning('Failed to fetch video details')
        return jsonify({'status': False, 'message': 'Failed to fetch video details'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    