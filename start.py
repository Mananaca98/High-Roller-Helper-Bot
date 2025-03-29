from bot_core import BigCatBot
import json

def main():
    with open('config.json') as f:
        config = json.load(f)
    
    bot = BigCatBot(token=config['telegram_token'])
    print("🐆 BigCat Bot iniciado...")
    bot.run()

if __name__ == '__main__':
    main()