import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("T8688404030:AAHeM7LBRolyLFQvVWBk7DWE44LKT8KA4AA")
TELEGRAM_CHAT_ID = os.getenv("8688404030")

MIN_SPREAD = float(os.getenv("MIN_SPREAD", 1))
MIN_VOLUME = float(os.getenv("MIN_VOLUME", 10000))
MAX_VOLUME = float(os.getenv("MAX_VOLUME", 100000000))

EXCHANGES = [
    "okx",
    "bybit",
    "mexc",
    "htx"
]

SCAN_INTERVAL = 300
