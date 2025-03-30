# prediction_engine.py
import websocket
import json
import numpy as np
from tensorflow import keras

class LiveDataScraper:
    def __init__(self, country="MZ"):
        self.ws_url = f"wss://{country.lower()}-casino-feed.com/live"  # Replace with real endpoint
        self.model = keras.models.load_model("mozambique_lstm.h5")

    def start_websocket_listener(self):
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self._on_message,
            on_error=self._on_error
        )
        ws.run_forever()

    def _on_message(self, ws, message):
        data = json.loads(message)
        prediction = self._predict(data)
        return prediction

    def _predict(self, live_data):
        # Preprocess data for LSTM input
        processed = np.array([[...]])  # Your preprocessing logic
        prediction = self.model.predict(processed)
        return {
            "multiplier": float(prediction[0][0]),
            "confidence": min(99, int(prediction[0][1] * 100))
        }