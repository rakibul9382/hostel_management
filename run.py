# run.py

from dotenv import load_dotenv
import os

# Load variables from .env file into the environment
load_dotenv() 

# Now import and run your app
from app import create_app
app=create_app()
if __name__ == '__main__':
     # Railway assigns a dynamic port
    port = int(os.environ.get("PORT", 5000))  # default 5000 for local dev
    # Listen on all interfaces
    app.run(host="0.0.0.0", port=port)