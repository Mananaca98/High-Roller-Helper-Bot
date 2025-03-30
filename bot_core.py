from telegram.ext import Application
import logging
import random

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class HighRollerHelperBot:
    def __init__(self, token: str, stealth_level: int = 3, country: str = "MZ"):
        self.application = Application.builder().token(token).build()
        from commands import BotCommands
        self.commands = BotCommands(self.application)
        logger.info(f"Bot initialized for {country}")

    def _init_commands(self):
        from commands import BotCommands
        self.commands = BotCommands(self.application)  # No need to store as attr    

    def run(self):
        try:
            self.application.run_polling()
        except Exception as e:
            logger.critical(f"Bot crashed: {str(e)}")
            raise