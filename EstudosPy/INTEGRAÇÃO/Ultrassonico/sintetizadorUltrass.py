import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard

porta = '/dev/ttyACM0'
amostragem = 44100
limiteDistancia = 30
volumeMaximo = 1.0

params = {
    'freq_alvo': 261.63,
    'freq_atual': 261.63,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0.0
}

ESCALA_MUSICAL = [
    (5, 261.63),  # Do
    (8, 293.66),  # Re
    (11, 329.63), # Mi
    (14, 349.23), # Fa
    (17, 392.00), # Sol
    (20, 440.00), # La
    (23, 493.88), # Si
    (float('inf'), 523.25) # Do2
]

try:
    porta = serial.Serial(porta, 9600, timeout=0.01)
except:
    print("Erro: Verifique se o Arduino está na porta /dev/ttyACM0")
    exit()

# while True:
#     linha = porta.readline().decode('utf-8', errors='ignore').strip()
#     dados = linha.split(',')
             
#     if len(dados) == 2: 
#         valor1 = dados[0]
#         valor2 = dados[1]
#         if valor1.isdigit() and valor2.isdigit():
#             print(f"Freq: {valor1} | Vol: {valor2}")

def audio_callback(outdata, frames, time, status):
    t = np.arange(frames) / amostragem
    
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    params['freq_atual'] += 0.05 * (params['freq_alvo'] - params['freq_atual'])
    
    f = params['freq_atual']
    v = params['vol_atual']
    
    arg = 2 * np.pi * f * t + params['fase']
    outdata[:, 0] = v * np.sin(arg)
    
    params['fase'] = (arg[-1] + (2 * np.pi * f / amostragem)) % (2 * np.pi)

def processar(leitura1, leitura2):
    if leitura1 <= limiteDistancia:
        diferenca = limiteDistancia - leitura1
        params['vol_alvo'] = (diferenca / limiteDistancia) * volumeMaximo
        
        for limiar, frequencia in ESCALA_MUSICAL:
            if leitura2 < limiar:
                params['freq_alvo'] = frequencia
                break
    else:
        params['vol_alvo'] = 0.0

def ao_pressionar(key):
    if key == keyboard.Key.esc:
        return False
    
with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem):
    with keyboard.Listener(on_press=ao_pressionar) as listener:
        print("Sintetizador rodando... Pressione ESC para sair.")
        try:
            while listener.running:
                linha = porta.readline().decode('utf-8', errors='ignore').strip()
                dados = linha.split(',')
                
                if len(dados) == 2: 
                    v1, v2 = dados[0], dados[1]
                    if v1.isdigit() and v2.isdigit():
                        try:
                            print(f"Freq: {v1} | Vol: {v2}")
                            processar(int(v1), int(v2))
                        except ValueError:
                            continue
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")