# Arduino está enviando dados da leitura de sombra do LRD.

import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard


# Configurações da Serial
try:
    porta = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
except:
    print("Erro: Verifique se o Arduino está na porta /dev/ttyACM0")
    exit()

# Configurações de Áudio
amostragem = 44100
limiteSombra = 250

params = {
    'freq': 440.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0
}

def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    
    # Suavização para evitar estalos
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames

def ao_pressionar(key):
    if key == keyboard.Key.esc:
        return False

with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar) as listener:
        while listener.running:
            dados = porta.readline().decode('utf-8').strip()
            if dados.isdigit():
                try:
                    valor = int(dados)
                    print(valor)
                    
                    if valor < limiteSombra:
                        params['vol_alvo'] = 2.0 
                    else:
                        params['vol_alvo'] = 0.0
                except:
                    pass