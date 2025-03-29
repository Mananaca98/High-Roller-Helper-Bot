from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv
import os
import logging

# Carrega as variáveis do .env
load_dotenv()

logger = logging.getLogger(__name__)

class BotCommands:
    def __init__(self, application):
        self.application = application
        # Carrega as configurações do .env para um dicionário em memória
        self.config = {
            "telegram_token": os.getenv("TELEGRAM_TOKEN"),
            "cassino": os.getenv("CASSINO", "Placard"),
            "auto_mode": os.getenv("AUTO_MODE", "false").lower() == "true",
            "min_confidence": int(os.getenv("MIN_CONFIDENCE", "75")),
            "admin_chat_ids": os.getenv("ADMIN_CHAT_IDS", "").split(",")
        }
        self._register_commands()

    def _register_commands(self):
        commands = [
            ('start', self.cmd_start),
            ('ajuda', self.cmd_ajuda),
            ('previsao', self.cmd_previsao),
            ('cassino', self.cmd_cassino),
            ('automatico', self.cmd_automatico),
            ('saldo', self.cmd_saldo),
            ('status', self.cmd_status),
            ('parar', self.cmd_parar),
            ('historico', self.cmd_historico),
            ('alertas', self.cmd_alertas),
            ('config', self.cmd_config)
        ]
        
        for cmd, handler in commands:
            self.application.add_handler(CommandHandler(cmd, handler))
        
        self.application.add_handler(
            CallbackQueryHandler(self.cassino_callback, pattern='^cassino_')
        )

    def _load_config(self):
        return self.config

    def _save_config(self, config):
        # Atualiza o dicionário de configuração em memória
        self.config = config

    def cmd_start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "🐅 *BigCat Bot Ativado!* 🐆\n"
            "Digite /ajuda para ver todos os comandos",
            parse_mode='Markdown'
        )

    def cmd_ajuda(self, update: Update, context: CallbackContext):
        help_text = [
            "❓ *AJUDA RÁPIDA* ❓",
            "/start - 🐅 Inicia o bot",
            "/previsao - 🔮 Próxima previsão",
            "/cassino - 🎰 Trocar casa de apostas",
            "/automatico - 🤖 Ativar modo automático",
            "/saldo - 💰 Ver saldo",
            "/parar - ⏸️ Pausar o bot",
            "/historico - 📜 Ver histórico",
            "/alertas - 🔔 Configurar alertas",
            "/config - ⚙️ Ajustes avançados"
        ]
        update.message.reply_text("\n".join(help_text), parse_mode='Markdown')

    def cmd_previsao(self, update: Update, context: CallbackContext):
        try:
            config = self._load_config()
            update.message.reply_text(
                "🔮 *PRÓXIMA PREVISÃO* 🔮\n"
                f"Multiplicador: 2.45x\n"
                f"Confiança: 82%\n"
                f"Casa atual: {config.get('cassino', 'Placard')}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erro previsao: {str(e)}")
            update.message.reply_text("⚠️ Erro ao gerar previsão")

    def cmd_cassino(self, update: Update, context: CallbackContext):
        keyboard = [
            [InlineKeyboardButton("🎰 Placard", callback_data='cassino_placard')],
            [InlineKeyboardButton("🎲 BetWay", callback_data='cassino_betway')],
            [InlineKeyboardButton("🏛️ Hollywoodbets", callback_data='cassino_hollywood')]
        ]
        update.message.reply_text(
            "🎰 *SELECIONE A CASA DE APOSTAS:*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    def cassino_callback(self, update: Update, context: CallbackContext):
        query = update.callback_query
        casa = query.data.split('_')[1]
        
        config = self._load_config()
        config['cassino'] = casa
        self._save_config(config)
        
        query.edit_message_text(f"✅ Casa alterada para: {casa.upper()}")

    def cmd_automatico(self, update: Update, context: CallbackContext):
        config = self._load_config()
        config['auto_mode'] = not config.get('auto_mode', False)
        self._save_config(config)
        
        status = "LIGADO" if config['auto_mode'] else "DESLIGADO"
        update.message.reply_text(f"🤖 MODO AUTOMÁTICO: {status}")

    def cmd_saldo(self, update: Update, context: CallbackContext):
        update.message.reply_text("💰 *SALDO ATUAL:* 1.245,00 MZN", parse_mode='Markdown')

    def cmd_status(self, update: Update, context: CallbackContext):
        config = self._load_config()
        update.message.reply_text(
            f"📊 *STATUS ATUAL*\n"
            f"Casa: {config.get('cassino', 'N/D')}\n"
            f"Automático: {'✅' if config.get('auto_mode') else '❌'}\n"
            f"Última aposta: 2.45x",
            parse_mode='Markdown'
        )

    def cmd_parar(self, update: Update, context: CallbackContext):
        update.message.reply_text("⏸️ O bot foi pausado com sucesso!", parse_mode='Markdown')

    def cmd_historico(self, update: Update, context: CallbackContext):
        update.message.reply_text("📜 *Histórico de apostas:* \n1. 2.45x\n2. 1.80x\n3. 3.00x", parse_mode='Markdown')

    def cmd_alertas(self, update: Update, context: CallbackContext):
        update.message.reply_text("🔔 *Configuração de Alertas:* \nAtivar/Desativar alertas de apostas", parse_mode='Markdown')

    def cmd_config(self, update: Update, context: CallbackContext):
        update.message.reply_text("⚙️ *Configurações Avançadas:* \nAjustes para personalizar a experiência do bot", parse_mode='Markdown')
