from bot_core import HighRollerHelperBot  # Certifique-se de que bot_core utiliza o token de .env também
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Erro: TELEGRAM_TOKEN não está definido no .env")
        return
    
    bot = HighRollerHelperBot(token=token)
    print("🐆 High Roller Helper Bot iniciado...")
    bot.run()

if __name__ == '__main__':
    main()
