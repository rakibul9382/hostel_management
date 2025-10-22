# run.py

from dotenv import load_dotenv
import os

# Load variables from .env file into the environment
load_dotenv() 

# Now import and run your app
from app import create_app
app=create_app()
if __name__ == '__main__':
    app.run(debug=True) # debug=True is good for development