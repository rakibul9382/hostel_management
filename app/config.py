# app/config.py

import os

class Config:
    """Contains all configurations for the Flask app."""
    
    # You should always have a secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'

    # Create your database config dictionary *once* here
    DB_CONFIG = {
        'user': os.environ.get("DB_USER"),
        'host': os.environ.get('DB_HOST'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get("DB_NAME")
    }
