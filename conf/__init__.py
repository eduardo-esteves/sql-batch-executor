import os
from pathlib import Path

from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

# Database settings
config = {
    'user': os.getenv('dbuser'),
    'password': os.getenv('dbpass'),
    'host': os.getenv('dbhost'),
    'database': os.getenv('dbname'),
    'raise_on_warnings': True
}

BASE_DIR = Path(__file__).resolve().parent.parent
