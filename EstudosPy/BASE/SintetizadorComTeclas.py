import numpy as np
import sounddevice as sd
from pynput import keyboard

amostragem = 44100
params = {
    'freq': 440.0,
    'vol': 3.0,
    'fase': 0
}

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
    
    outdata[:, 0] = params['vol'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    
    params['fase'] += frames

def ao_pressionar(key):
    try:
        if key.char in notas:
            params['freq'] = notas[key.char]
            params['vol'] = 0.8  # Valor bruto
    except AttributeError:
        pass

def ao_soltar(key):
    params['vol'] = 0.0
    if key == keyboard.Key.esc:
        return False

print("Toque A, S, D, F, G, H, J, K | Esc para sair")

with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        listener.join()
