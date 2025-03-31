import os
import time
import numpy as np
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AviatorBot:
    def __init__(self):
        self.driver = self._init_stealth_browser()
        self.model = tf.keras.models.load_model('aviator_lstm_earth_v5.h5')
        self._login()

    def _init_stealth_browser(self):
        options = Options()
        options.add_argument(f"user-agent={os.getenv('USER_AGENT')}")
        options.add_argument(f"--proxy-server={os.getenv('PROXY_LIST').split(',')[0]}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _login(self):
        self.driver.get(os.getenv("LOGIN_URL"))
        time.sleep(2)
        
        # Human-like typing
        self._human_type(By.ID, "username", os.getenv("USERNAME"))
        self._human_type(By.ID, "password", os.getenv("PASSWORD"))
        
        # Random mouse movement before click
        button = self.driver.find_element(By.ID, "login-button")
        ActionChains(self.driver).move_to_element(button).pause(1).click().perform()
        
        # Wait for game to load
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("game-play")
        )

    def _human_type(self, by, identifier, text):
        element = self.driver.find_element(by, identifier)
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
            if random.random() < 0.05:  # 5% chance of typo
                element.send_keys(random.choice("abcdefghijklmnopqrstuvwxyz"))
                time.sleep(0.5)
                element.send_keys("\b")

    def get_round_data(self):
        return self.driver.execute_script("""
            return {
                history: window.gameState.history.slice(-15),
                nextRound: Date.now() + 3000,
                currentMultiplier: document.querySelector('.multiplier-counter').innerText
            }
        """)

    def predict_next_round(self):
        data = self.get_round_data()
        prediction = self.model.predict(np.array([data['history']]))
        
        return {
            'crash_point': float(prediction[0][0]),
            'confidence': float(prediction[0][1] * 100),
            'timestamp': data['nextRound']
        }