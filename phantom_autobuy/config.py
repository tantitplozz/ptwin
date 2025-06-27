import os
from dotenv import load_dotenv

load_dotenv()

# GoLogin Configuration
GOLOGIN_API_KEY = os.getenv("GOLOGIN_API_KEY")
GOLOGIN_PROFILE_ID = os.getenv("GOLOGIN_PROFILE_ID")

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Database & Storage
VECTORDB_PATH = os.getenv("VECTORDB_PATH", "./vector_db.json")
CARD_PROFILES = os.getenv("CARD_PROFILES", "cards.json")

# Monitor Configuration
MONITOR_PORT = int(os.getenv("MONITOR_PORT", "8686"))
MONITOR_HOST = os.getenv("MONITOR_HOST", "0.0.0.0")

# Payment Configuration
PAYMENT_CARD_NUMBER = os.getenv("PAYMENT_CARD_NUMBER")
PAYMENT_EXP = os.getenv("PAYMENT_EXP")
PAYMENT_CVV = os.getenv("PAYMENT_CVV")
PAYMENT_NAME = os.getenv("PAYMENT_NAME", "John Doe")

# OTP Configuration
OTP_API_KEY = os.getenv("OTP_API_KEY")
OTP_SERVICE = os.getenv("OTP_SERVICE", "auto")

# Browser Configuration
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))

# A/B Testing Configuration
AB_TEST_PROFILES = int(os.getenv("AB_TEST_PROFILES", "3"))
AB_TEST_ITERATIONS = int(os.getenv("AB_TEST_ITERATIONS", "1"))

# Stealth Configuration
STEALTH_MODE = os.getenv("STEALTH_MODE", "true").lower() == "true"
HUMAN_DELAY_MIN = int(os.getenv("HUMAN_DELAY_MIN", "1000"))
HUMAN_DELAY_MAX = int(os.getenv("HUMAN_DELAY_MAX", "5000"))

# Target Product Configuration
TARGET_PRODUCT = os.getenv("TARGET_PRODUCT", "iPhone 16 Pro Max")
TARGET_STORAGE = os.getenv("TARGET_STORAGE", "1TB")
TARGET_COLOR = os.getenv("TARGET_COLOR", "Natural Titanium")
TARGET_CARRIER = os.getenv("TARGET_CARRIER", "Unlocked")