import os
from telegram import Bot
from telegram.constants import ParseMode

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
        
    def send_prediction(self, round_id, prediction, confidence):
        message = (
            f"🚀 *AVIATOR PREDICTION ALERT* 🚀\n\n"
            f"🆔 Round: `{round_id}`\n"
            f"📊 Predicted Multiplier: `{prediction:.2f}x`\n"
            f"🎯 Confidence: `{confidence:.1f}%`\n\n"
            f"_Threshold: {os.getenv('MIN_CONFIDENCE')}%_"
        )
        for chat_id in eval(os.getenv('ADMIN_CHAT_IDS')):
            self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )