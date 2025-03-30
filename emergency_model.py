# emergency_model.py
import numpy as np # type: ignore
from tensorflow import keras # type: ignore

def create_emergency_model():
    model = keras.Sequential([
        keras.layers.LSTM(64, input_shape=(10, 5)),
        keras.layers.Dense(2, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Save temporary model
create_emergency_model().save("mozambique_lstm.h5")