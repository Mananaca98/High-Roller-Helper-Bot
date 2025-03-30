from telegram.ext import Application
from commands import BotCommands
from selenium_stealth import stealth
import logging

class HighRollerHelperBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.commands = BotCommands(self.application)
        self._configure_stealth()

    def _configure_stealth(self):
        """Initialize stealth configurations"""
        self.stealth_params = {
            "languages": ["pt-PT", "pt"],
            "vendor": "Google Inc.",
            "platform": "Win32",
            "webgl_vendor": "Intel Inc.",
            "renderer": "Intel Iris OpenGL Engine",
        }

    def run(self):
        """Start the bot with stealth enhancements"""
        try:
            self.application.run_polling(
                poll_interval=1.5,
                timeout=30,
                drop_pending_updates=True
            )
        except Exception as e:
            logging.error(f"Polling error: {str(e)}")
            raise