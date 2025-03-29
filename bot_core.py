#from telegram import Bot
from telegram.ext import Application
from commands import BotCommands

class HighRollerHelperBot:
    def __init__(self, token: str):
        # Criação da instância da aplicação, não do updater
        self.application = Application.builder().token(token).build()
        
        # Passar a instância da aplicação para o BotCommands
        self.commands = BotCommands(self.application)
    
    def run(self):
        # Inicia a aplicação
        self.application.run_polling()

