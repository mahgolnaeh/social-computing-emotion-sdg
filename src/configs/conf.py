import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads from ../..env when running from src

API_KEY_OAI = os.getenv("OPENROUTER_API_KEY")

if API_KEY_OAI is None:
    raise ValueError("API_KEY_OAI not found. Please set OPENROUTER_API_KEY in your ..env file.")
