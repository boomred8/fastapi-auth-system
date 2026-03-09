import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
secret_key = os.getenv('MY_SECRET_KEY')

if not database_url:
    raise ValueError('DATABASE_URL environment variable is not set')
if not secret_key:
    raise ValueError('MY_SECRET_KEY environment variable is not set')