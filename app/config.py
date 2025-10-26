# app/config.py

import os

class Config:
    """Contains all configurations for the Flask app."""
    
    # You should always have a secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-string'
    UPLOAD_FOLDER=os.path.join('app','static','uploads')
    ALLOWED_EXTENSIONS={'png','jpg','jpeg'}
    MAX_CONTENT_LENGTH=2*1024*1024  #max 2MB per file

    # Create your database config dictionary *once* here
    DB_CONFIG = {
        'user': os.environ.get("DB_USER"),
        'host': os.environ.get('DB_HOST'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get("DB_NAME"),
        'port':os.environ.get("DB_PORT")
    }
