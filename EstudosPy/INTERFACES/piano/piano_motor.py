import numpy as np
import sounddevice as sd
from pynput import keyboard
import matplotlib.pyplot as plt
from queue import Queue

# --- CONFIGURAÇÕES DO ÁUDIO ---
amostragem = 44100
CHUNK = 1024 * 2 # Tamanho do bloco que vamos mostrar no gráfico

params = {
    'freq': 440.0,
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'fase': 0
}

notas = {
    'a': 261.63, 's': 293.66, 'd': 329.63, 'f': 349.23,
    'g': 392.00, 'h': 440.00, 'j': 493.88, 'k': 523.25
}

# Fila para transferir os dados do áudio para o gráfico
fila_onda = Queue()

def audio_callback(outdata, frames, time_info, status):
    indices = np.arange(frames) + params['fase']
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    # onda
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames
    
    # Copiar os dados para o gráfico ler
    fila_onda.put(onda.copy())

# --- CONFIGURAÇÃO DO GRÁFICO (MATPLOTLIB) ---
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=2, color='cyan')

ax.set_facecolor('black') 
fig.patch.set_facecolor('black')
ax.set_ylim(-1.1, 1.1) 
ax.set_xlim(0, CHUNK)
ax.get_xaxis().set_visible(False) 

plt.show(block=False)

# --- FUNÇÕES DO TECLADO ---
def ao_pressionar(key):
    try:
        if key.char in notas:
            params['freq'] = notas[key.char]
            params['vol_alvo'] = 0.8 
    except AttributeError: pass

def ao_soltar(key):
    params['vol_alvo'] = 0.0
    if key == keyboard.Key.esc: return False

# --- LOOP ---
with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem, blocksize=CHUNK):
    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        print("Sintetizador com Gráfico Ativo! Pressione A-K. ESC para sair.")
        
        while listener.running:
            if not fila_onda.empty():
                dados_da_onda = fila_onda.get()
                line.set_ydata(dados_da_onda)
                
                fig.canvas.draw()
                fig.canvas.flush_events()
            
            plt.pause(0.01)