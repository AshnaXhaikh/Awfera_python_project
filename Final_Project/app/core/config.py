# app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("D:/awfera/Final_Project/.env" if os.path.exists("D:/awfera/Final_Project/.env") else ".env")

# Get the API key from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")