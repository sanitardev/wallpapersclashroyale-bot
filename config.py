import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

URL = "https://squid-app-tiggw.ondigitalocean.app/"
API_URL = "https://164.92.229.214/"
CRT_PATH = '.crt/ca_bundle.crt'
ADMIN = os.getenv("ADMIN")
