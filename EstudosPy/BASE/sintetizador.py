import numpy as np
import sounddevice as sd

# Configurações globais
amostragem = 44100

params = {
    'freq': 440.0,
    'vol': 0.8,
    'fase': 0
}

def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    
    outdata[:, 0] = params['vol'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    
    params['fase'] += frames

print("Pressione Enter para desligar.")

try:
    with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
        while True:
            nova_freq = input("Digite uma nova frequência ou Enter para sair: ")
            if nova_freq == "":
                break
            params['freq'] = float(nova_freq)
except Exception as e:
    pass