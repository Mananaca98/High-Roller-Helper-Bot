import numpy as np
from tensorflow.keras.models import load_model

class AviatorPredictor:
    def __init__(self):
        self.model = load_model('brain/lstm_model.h5')
        self.window_size = 20  # Last 20 rounds
        
    def preprocess(self, raw_data):
        # Convert to 3D array (samples, timesteps, features)
        X = np.array([
            [round['multiplier'] for round in raw_data[-self.window_size:]],
            [round['time_since_last'] for round in raw_data[-self.window_size:]],
            [round['day_part'] for round in raw_data[-self.window_size:]]
        ]).T
        return X.reshape(1, self.window_size, 3)
        
    def predict(self, current_round_data):
        X = self.preprocess(current_round_data)
        return self.model.predict(X)[0][0] * 0.99  # 1% safety factor
    
    # Add to feature_engine.py
def _enhance_accuracy(self):
    # Mozambique-specific time patterns
    self.time_weights = {
        'morning': 0.7,    # 06:00-11:00
        'afternoon': 1.2,   # 12:00-15:00
        'evening': 1.5,     # 16:00-20:00
        'night': 0.9        # 21:00-05:00
    }
    # Cultural event detection
    self.holiday_boost = {
        'Dia da Independência': 1.3,  # June 25
        'Ano Novo': 1.4               # Jan 1
    }