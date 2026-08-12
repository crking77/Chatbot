import os
from dotenv import load_dotenv
from datetime import timedelta
import  json
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  

FACEBOOK_PAGE_TOKENS = json.loads(os.getenv("FACEBOOK_PAGE_TOKENS", "{}"))