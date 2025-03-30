from bot_core import HighRollerHelperBot
from dotenv import load_dotenv
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_runtime.log')
    ]
)

def initialize_services():
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not found in .env")
        sys.exit(1)

    # SAFE CONFIG PARSING
    try:
        stealth_level = int(os.getenv("STEALTH_LEVEL", "3").split()[0])  # Takes first number only
        country = os.getenv("COUNTRY", "MZ").upper().strip()
    except Exception as e:
        logging.error(f"Config parse error: {e}")
        stealth_level = 3  # Default fallback
        country = "MZ"
    
    return token, stealth_level, country

def main():
    try:
        token, stealth_level, country = initialize_services()
        
        bot = HighRollerHelperBot(
            token=token,
            stealth_level=stealth_level,
            country=country
        )
        
        logging.info(f"🐆 Starting High Roller Helper Bot (Stealth Level: {stealth_level}, Country: {country})")
        bot.run()
        
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()