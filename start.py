from bot_core import HighRollerHelperBot
from dotenv import load_dotenv
import os
import logging
from prediction.prediction_engine import LiveDataScraper  # New correct path
import numpy as np

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def main():
    # Pega o token do ambiente
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not found in .env")
        return

    # Obtém os parâmetros de stealth_level e country (padrão para "MZ")
    stealth_level = int(os.getenv("STEALTH_LEVEL", 0))  # Default para 0
    country = os.getenv("COUNTRY", "MZ")  # Default para "MZ"

    try:
        # Inicializa o bot com os parâmetros necessários
        bot = HighRollerHelperBot(token=token, stealth_level=stealth_level, country=country)
        logging.info("🐆 High Roller Helper Bot starting...")

        # Inicia o scraper de dados em tempo real
        scraper = LiveDataScraper(country=country)
        scraper.start_websocket_listener()

        # Executa o bot
        bot.run()
    except Exception as e:
        logging.critical(f"Bot crashed: {str(e)}")

# Certifique-se de que a função main seja chamada corretamente
if __name__ == '__main__':
    main()
