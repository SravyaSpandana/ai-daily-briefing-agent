import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY and os.getenv("APP_ENV") != "test":
    raise ValueError(
        "GOOGLE_API_KEY is not configured. Please add it to your .env file."
    )