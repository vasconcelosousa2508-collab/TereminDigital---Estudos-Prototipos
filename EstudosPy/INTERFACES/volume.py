import numpy as np
import sounddevice as sd
from pynput import keyboard

# Configurações
amostragem = 44100

params = {
    'freq': 0.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'vol_maximo': 1.0,
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

volumes = {'1': 0.1, '2': 0.2, '3': 0.3, '4': 0.4, '5': 0.5, '6': 0.6, '7': 0.7, '8': 0.8, '9': 0.9, '0': 1.0,
           'z': 0.15, 'x': 0.25, 'c': 0.35, 'v': 0.45, 'b': 0.55, 'n': 0.65, 'm': 0.75, ',': 0.85, '.': 0.95, '/': 0.0} 

def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    
    # Suavização 
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames

def ao_pressionar(key):
    try:
        if key.char in volumes:
            params['vol_maximo'] = volumes[key.char]
        elif key.char in notas:
            params['freq'] = notas[key.char]
            params['vol_alvo'] = params['vol_maximo']
    except AttributeError:
        pass

def ao_soltar(key):
    try: 
        if key.char in notas:
            params['vol_alvo'] = 0.0
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        return False

print("--- PIANO TURBINADO (VOL 2.0) ---")
print("Toque A, S, D, F, G, H, J, K | Esc para sair")

with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        listener.join()
