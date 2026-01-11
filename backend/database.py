import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    print("WARNING: MONGODB_URL not found in environment variables.")
    # Fallback or error handling - for now we proceed but standard ops will fail
    client = None
    db = None
else:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    db = client.civicvoice_db  # Using a default database name 'civicvoice_db'
