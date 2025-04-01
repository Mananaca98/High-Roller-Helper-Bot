import json
from datetime import datetime
from dotenv import load_dotenv
from stealth.proxy_rotator import ProxyManager
from stealth.human_emulator import HumanEmulator
from brain.feature_engine import AviatorPredictor
from telegram_alert import TelegramNotifier

load_dotenv()

class CasinoBot:
    def __init__(self):
        self.driver = ProxyManager().get_driver()
        self.predictor = AviatorPredictor()
        self.notifier = TelegramNotifier()
        self.round_history = []
        
    def login(self):
        HumanEmulator.random_delay()
        self.driver.get(os.getenv('AVIATOR_URL'))
        
        phone_field = self.driver.find_element('id', 'phoneNumber')
        HumanEmulator.human_typing(phone_field, os.getenv('USERNAME'))
        
        password_field = self.driver.find_element('id', 'password')
        HumanEmulator.human_typing(password_field, os.getenv('PASSWORD'))
        
        login_btn = self.driver.find_element('xpath', '//button[contains(text(),"INICIAR SESSÃO")]')
        HumanEmulator.mouse_movement(self.driver)
        login_btn.click()

    def monitor_rounds(self):
        while True:
            current_round = self._scrape_round_data()
            if current_round['id'] not in [r['id'] for r in self.round_history]:
                self.round_history.append(current_round)
                prediction, confidence = self.predictor.predict(self.round_history)
                
                if confidence >= float(os.getenv('MIN_CONFIDENCE')):
                    self.notifier.send_prediction(
                        current_round['id'],
                        prediction,
                        confidence
                    )
                    self._place_bet(prediction)
                    
            HumanEmulator.random_delay(1, 3)

if __name__ == "__main__":
    bot = CasinoBot()
    bot.login()
    bot.monitor_rounds()