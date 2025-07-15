from dotenv import load_dotenv
from flask import Flask
import os
import sys

from filters import filesize_filter, datetime_filter
from routes import register_routes

load_dotenv()

USERNAME = os.getenv('AUTH_USERNAME')
PASSWORD = os.getenv('AUTH_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)

if not USERNAME or not PASSWORD:
    print("❌ Error: AUTH_USERNAME and AUTH_PASSWORD must be set in the environment.", file=sys.stderr)
    sys.exit(1)

app = Flask(__name__)
app.secret_key = SECRET_KEY
STORAGE_DIR = 'storage'
os.makedirs(STORAGE_DIR, exist_ok=True)

app.template_filter('filesize')(filesize_filter)
app.template_filter('format_datetime')(datetime_filter)

register_routes(app, STORAGE_DIR, USERNAME, PASSWORD)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
