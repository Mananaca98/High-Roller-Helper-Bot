from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import asyncio
import logging
from bot_core import AviatorBot

logger = logging.getLogger(__name__)

class AviatorCommands:
    def __init__(self, app):
        self.bot = AviatorBot()
        self.app = app
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("predict", self.predict))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🌍 EARTH DEFENSE SYSTEM ACTIVATED 🌍")

    async def predict(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        while True:
            try:
                prediction = self.bot.predict_next_round()
                if prediction['confidence'] >= float(os.getenv("MIN_CONFIDENCE")):
                    await self._send_alert(update, prediction)
                await asyncio.sleep(float(os.getenv("PREDICTION_WINDOW")))
            except Exception as e:
                logger.error(f"PREDICTION FAILURE: {str(e)}")

    async def _send_alert(self, update: Update, data):
        alert_msg = (
            f"🚨 EARTH ALERT 🚨\n"
            f"Next crash: {data['crash_point']:.2f}x\n"
            f"Confidence: {data['confidence']:.2f}%\n"
            f"Impact in: {os.getenv('PREDICTION_WINDOW')}s"
        )
        await update.message.reply_text(alert_msg)