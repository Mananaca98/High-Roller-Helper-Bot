
### STEP 3: STEALTH LOGIN SYSTEM (stealth/human_emulator.py)
import random
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

class HumanEmulator:
    @staticmethod
    def random_delay(min=0.5, max=2.3):
        sleep(random.uniform(min, max))
    
    @staticmethod
    def human_typing(element, text):
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.08, 0.15))  # Mozambique typing speed
            
    @staticmethod
    def mouse_movement(driver):
        action = ActionChains(driver)
        for _ in range(random.randint(2,5)):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            action.move_by_offset(x, y).perform()
            sleep(random.uniform(0.2, 0.7))