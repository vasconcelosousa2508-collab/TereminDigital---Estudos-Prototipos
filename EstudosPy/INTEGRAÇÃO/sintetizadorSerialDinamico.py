import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard


porta_nome = '/dev/ttyACM0'
amostragem = 44100
limiteSombra = 380

# Estado global
params = {
    'freq': 440.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0
}

# (Limiar, Frequência)
MAPA_NOTAS = [
    (150, 261.63), (180, 293.66), (210, 329.63), 
    (240, 349.23), (270, 392.00), (310, 440.00), 
    (350, 493.88), (float('inf'), 523.25)
]

try:
    porta = serial.Serial(porta_nome, 9600, timeout=0.1)
except:
    print("Erro: Verifique se o Arduino está na porta /dev/ttyACM0")
    exit()


def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    # Suavização de ganho para evitar estalos
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames

def processar(valor):
    if valor < limiteSombra:
        params['vol_alvo'] = 0.5
        for limiar, f in MAPA_NOTAS:
            if valor < limiar:
                params['freq'] = f
                break
    else:
        params['vol_alvo'] = 0.0

def ao_pressionar(key):
    if key == keyboard.Key.esc:
        return False


with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar) as listener:
        while listener.running:
            dados = porta.readline().decode('utf-8', errors='ignore').strip()
            if dados.isdigit():
                valor = int(dados)
                print(valor)
                processar(valor)