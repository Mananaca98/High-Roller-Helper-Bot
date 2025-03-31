from telegram.ext import Application
from commands import AviatorCommands
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('earth_defense.log'),
            logging.StreamHandler()
        ]
    )

    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    AviatorCommands(app)
    
    logging.info("🔥 EARTH PROTECTION PROTOCOL INITIATED 🔥")
    app.run_polling()

if __name__ == '__main__':
    main()