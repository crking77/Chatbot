import os
from dotenv import load_dotenv
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")