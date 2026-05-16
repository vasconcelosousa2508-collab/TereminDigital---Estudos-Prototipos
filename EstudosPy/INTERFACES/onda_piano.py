import numpy as np
import sounddevice as sd
from pynput import keyboard
import matplotlib.pyplot as plt
from queue import Queue

# --- CONFIGURAÇÕES ---
amostragem = 44100
CHUNK = 1024 * 2 

# O azul escuro exato da sua imagem de referência
COR_FUNDO_HEX = '#0b032c'

params = {
    'freq': 261.63, 
    'vol_alvo': 0.0,
    'vol_atual': 0.0,
    'vol_maximo': 1.0,
    'fase': 0
}

notas = {
    'a': 261.63, 's': 293.66, 'd': 329.63, 'f': 349.23,
    'g': 392.00, 'h': 440.00, 'j': 493.88, 'k': 523.25
}

volumes = {
    '1': 0.1, '2': 0.2, '3': 0.3, '4': 0.4, '5': 0.5, '6': 0.6, '7': 0.7, '8': 0.8, '9': 0.9, '0': 1.0,
    'z': 0.15, 'x': 0.25, 'c': 0.35, 'v': 0.45, 'b': 0.55, 'n': 0.65, 'm': 0.75, ',': 0.85, '.': 0.95, '/': 0.0
} 

fila_onda = Queue()

# --- MAPA DE CORES REAJUSTADO PARA O FUNDO AZUL ESCURO ---
escala_cores = [
    (261.63, (255, 0, 90)),    # Dó - Vermelho Neon Vibrante
    (293.66, (255, 125, 0)),   # Ré - Laranja Elétrico
    (329.63, (230, 255, 0)),   # Mi - Amarelo Neon
    (349.23, (0, 255, 140)),   # Fá - Verde Mentolado
    (392.00, (0, 235, 255)),   # Sol - Ciano Puro
    (440.00, (80, 140, 255)),  # Lá - Azul Elétrico (Clareado para dar contraste)
    (493.88, (210, 90, 255)),  # Si - Roxo Claro Ultravioleta (Aumentado o brilho)
    (523.25, (255, 0, 190))    # Dó Agudo - Rosa Choque Synthwave
]

def obter_cor_da_frequencia(freq):
    # 1. Se for menor ou igual à primeira nota (Dó grave), retorna Vermelho
    if freq <= escala_cores[0][0]:
        r, g, b = escala_cores[0][1]
        return f"#{r:02x}{g:02x}{b:02x}"
        
    # 2. Se for maior ou igual à última nota (Dó agudo), retorna Rosa Choque
    if freq >= escala_cores[-1][0]:
        r, g, b = escala_cores[-1][1]
        return f"#{r:02x}{g:02x}{b:02x}"
        
    # 3. Procura o intervalo entre as notas
    for i in range(len(escala_cores) - 1):
        f_inf, cor_inf = escala_cores[i]
        f_sup, cor_sup = escala_cores[i+1]
        
        if f_inf <= freq <= f_sup:
            fator = (freq - f_inf) / (f_sup - f_inf)
            r = int(cor_inf[0] + (cor_sup[0] - cor_inf[0]) * fator)
            g = int(cor_inf[1] + (cor_sup[1] - cor_inf[1]) * fator)
            b = int(cor_inf[2] + (cor_sup[2] - cor_inf[2]) * fator)
            return f"#{r:02x}{g:02x}{b:02x}"
            
    # SEDA DE SEGURANÇA: Se escapar por erro de arredondamento, retorna a última cor válida
    r, g, b = escala_cores[-1][1]
    return f"#{r:02x}{g:02x}{b:02x}"

# --- MOTOR DE ÁUDIO ---
def audio_callback(outdata, frames, time_info, status):
    indices = np.arange(frames) + params['fase']
    params['vol_atual'] += 0.1 * (params['vol_alvo'] - params['vol_atual'])
    
    onda = params['vol_atual'] * np.sin(2 * np.pi * params['freq'] * indices / amostragem)
    outdata[:, 0] = onda
    params['fase'] += frames
    
    fila_onda.put(onda.copy())

# --- CONFIGURAÇÃO VISUAL DO GRÁFICO ---
plt.rcParams['toolbar'] = 'None' 

fig, ax = plt.subplots(figsize=(10, 4))
fig.canvas.manager.set_window_title('Osciloscópio Cyberpunk')

x = np.arange(0, CHUNK)
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=3, color='#ff005a') 

# Aplicando o seu fundo azul customizado
ax.set_facecolor(COR_FUNDO_HEX)
fig.patch.set_facecolor(COR_FUNDO_HEX)

ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, CHUNK)
ax.axis('off') 

plt.show(block=False)

def ao_pressionar(key):
    try:
        letra = key.char
        if letra in volumes:
            params['vol_maximo'] = volumes[letra]
        elif letra in notas:
            params['freq'] = notas[letra]
            params['vol_alvo'] = params['vol_maximo']
    except AttributeError: pass

def ao_soltar(key):
    try: 
        if key.char in notas:
            params['vol_alvo'] = 0.0
    except AttributeError: pass
    if key == keyboard.Key.esc:
        return False

# --- LOOP PRINCIPAL DE RENDERIZAÇÃO ---
with sd.OutputStream(channels=1, callback=audio_callback, samplerate=amostragem, blocksize=CHUNK):
    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        while listener.running:
            dados_da_onda = None
            while not fila_onda.empty():
                dados_da_onda = fila_onda.get() 
            
            if dados_da_onda is not None:
                line.set_ydata(dados_da_onda)
                
                # PROTEÇÃO CONTRA BUG: Só muda a cor se o volume for real (evita conflito de thread)
                if params['vol_atual'] > 0.001:
                    cor_dinamica = obter_cor_da_frequencia(params['freq'])
                    line.set_color(cor_dinamica)
                
                try:
                    fig.canvas.draw_idle() 
                    fig.canvas.flush_events() 
                except:
                    break
            
            # Substituição do plt.pause por um loop de eventos nativo muito mais estável
            fig.canvas.start_event_loop(0.005)