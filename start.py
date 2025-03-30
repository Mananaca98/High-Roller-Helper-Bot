from bot_core import HighRollerHelperBot
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not found in .env")
        return
    
    try:
        bot = HighRollerHelperBot(token=token)
        logging.info("🐆 High Roller Helper Bot starting...")
        bot.run()
    except Exception as e:
        logging.critical(f"Bot crashed: {str(e)}")

if __name__ == '__main__':
    main()