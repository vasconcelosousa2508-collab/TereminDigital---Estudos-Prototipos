import numpy as np
import sounddevice as sd
from pynput import keyboard

# Configurações
amostragem = 44100

params = {
    'freq': 440.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0
}

# Notas (Frequências reais)
# Notas (Naturais e Sustenidos intercalados)
notas = {
    # Naturais
    'a': 261.63, 's': 293.66, 'd': 329.63, 'f': 349.23,
    'g': 392.00, 'h': 440.00, 'j': 493.88, 'k': 523.25,
    
    # Sustenidos (Teclas pretas - w, e, r, t, y)
    'w': 277.18, # C#
    'e': 311.13, # D#
    'r': 369.99, # F#
    't': 415.30, # G#
    'y': 466.16  # A#
}

def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    
    # Suavização 
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames

def ao_pressionar(key):
    try:
        if key.char in notas:
            params['freq'] = notas[key.char]
            params['vol_alvo'] = 0.8 
    except AttributeError:
        pass

def ao_soltar(key):
    params['vol_alvo'] = 0.0
    if key == keyboard.Key.esc:
        return False

print("--- PIANO TURBINADO (VOL 2.0) ---")
print("Toque A, S, D, F, G, H, J, K | Esc para sair")

with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        listener.join()
