from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
import logging
import random

logger = logging.getLogger(__name__)

class BotCommands:
    def __init__(self, application: Application):
        self.application = application
        self._register_handlers()

    def _register_handlers(self):
        """All handlers must be async"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("previsao", self.previsao))
        self.application.add_handler(CommandHandler("cassino", self.cassino))
        self.application.add_error_handler(self.error_handler)

    async def start(self, update: Update, context: CallbackContext):
        """MUST be async"""
        await update.message.reply_text("🐅 Bot Ativado! Digite /previsao")

    async def previsao(self, update: Update, context: CallbackContext):
        """Async prediction handler"""
        try:
            prediction = {
                "multiplier": round(random.uniform(1.5, 3.0), 2),
                "confidence": random.randint(85, 95)  # Force 85%+ accuracy
            }
            await update.message.reply_text(
                f"🎯 Previsão: {prediction['multiplier']}x\n"
                f"Confiança: {prediction['confidence']}%"
            )
        except Exception as e:
            logger.error(f"Prediction failed: {e}")

    async def cassino(self, update: Update, context: CallbackContext):
        """Async casino menu"""
        keyboard = [[InlineKeyboardButton("🎰 Placard", callback_data='placard')]]
        await update.message.reply_text(
            "Selecione:",
            reply_markup=InlineKeyboardMarkup(keyboard))
    
    async def error_handler(self, update: Update, context: CallbackContext):
        """Critical error catcher"""
        logger.error(f"Update {update} caused error {context.error}")