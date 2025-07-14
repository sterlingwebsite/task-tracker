from flask import Flask, flash, redirect, url_for
from auth import auth_bp
from tasks import tasks_bp
from models import init_db
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Secure key from .env

init_db()  # Initialize the user table

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

# Define root route before the app runs
@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # or 'tasks.dashboard'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # use Railway's assigned port
    app.run(debug=True, host='0.0.0.0', port=port)
