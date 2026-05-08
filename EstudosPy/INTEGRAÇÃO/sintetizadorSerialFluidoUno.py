import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard

# --- 1. CONFIGURAÇÕES ---
porta = '/dev/ttyACM0'
amostragem = 44100
limiteSombra = 380

params = {
    'freq_alvo': 261.63,
    'freq_atual': 261.63,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0.0
}

# Notas: Do, Re, Mi, Fa, Sol, La, Si, Do2
ESCALA_MUSICAL = [
    (150, 261.63), (180, 293.66), (210, 329.63), 
    (240, 349.23), (270, 392.00), (310, 440.00), 
    (350, 493.88), (float('inf'), 523.25)
]

try:
    porta = serial.Serial(porta, 9600, timeout=0.01)
except:
    print("Erro: Verifique se o Arduino está na porta /dev/ttyACM0")
    exit()



def audio_callback(outdata, frames, time, status):
    t = np.arange(frames) / amostragem
    
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    params['freq_atual'] += 0.05 * (params['freq_alvo'] - params['freq_atual'])
    
    f = params['freq_atual']
    v = params['vol_atual']
    
    arg = 2 * np.pi * f * t + params['fase']
    outdata[:, 0] = v * np.sin(arg)
    
    params['fase'] = (arg[-1] + (2 * np.pi * f / amostragem)) % (2 * np.pi)

def processar(leitura):
    if leitura < limiteSombra:
        params['vol_alvo'] = 0.5
        
        for limiar, frequencia in ESCALA_MUSICAL:
            if leitura < limiar:
                params['freq_alvo'] = frequencia
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
                print(f" {valor} | {params['freq_atual']:.2f}Hz")
                processar(valor)