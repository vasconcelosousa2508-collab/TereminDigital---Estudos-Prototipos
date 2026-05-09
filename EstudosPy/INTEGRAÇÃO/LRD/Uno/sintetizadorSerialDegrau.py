import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard

# --- 1. CONFIGURAÇÕES ---
porta = '/dev/ttyACM0'
amostragem = 44100
limiteSombra = 380

params = {
    'freq': 440.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0
}

# Notas: Do, Re, Mi, Fa, Sol, La, Si, Do2
ESCALA_MUSICAL = [
    (150, 261.63), (180, 293.66), (210, 329.63), 
    (240, 349.23), (270, 392.00), (310, 440.00), 
    (350, 493.88), (float('inf'), 523.25)
]

try:
    porta = serial.Serial(porta, 9600, timeout=0.1)
except:
    print("Erro: Verifique se o Arduino está na porta /dev/ttyACM0")
    exit()

def audio_callback(outdata, frames, time, status):
    indices = np.arange(frames) + params['fase']
    
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    # Geração da onda senoidal
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    
    outdata[:, 0] = onda
    params['fase'] += frames

def processar(leitura):
    if leitura < limiteSombra:
        params['vol_alvo'] = 0.5  
        
        for limiar, frequencia in ESCALA_MUSICAL:
            if leitura < limiar:
                params['freq'] = frequencia
                break
    else:
        params['vol_alvo'] = 0.0

def ao_pressionar(key):
    if key == keyboard.Key.esc:
        return False
    

with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar) as listener:
        while listener.running:
            linha = porta.readline().decode('utf-8', errors='ignore').strip()
            
            if linha.isdigit():
                valor = int(linha)
                print(f" {valor} | {params['freq']}Hz")
                processar(valor)