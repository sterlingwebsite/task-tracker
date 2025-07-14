from flask import Flask, flash
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

if __name__ == '__main__':
    app.run(debug=True)
