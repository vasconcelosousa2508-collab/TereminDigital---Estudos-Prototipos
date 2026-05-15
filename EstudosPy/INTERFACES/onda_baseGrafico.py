import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot 
import matplotlib.pyplot as plt
import time
from tkinter import TclError

matplotlib.use('TkAgg')

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second
# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting (X agora vai de 0 até 2047, correspondendo perfeitamente aos dados)
x = np.arange(0, CHUNK)

# create a line object with zeros instead of random numbers
line, = ax.plot(x, np.zeros(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(-32768, 32767)
ax.set_xlim(0, CHUNK)
plt.setp(ax, xticks=[0, CHUNK//2, CHUNK], yticks=[-32768, 0, 32767])

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    # 1. Lê os dados binários do microfone
    data = stream.read(CHUNK, exception_on_overflow=False)  
    
    # 2. Converte direto de binário para int16 (muito mais rápido que o struct)
    data_np = np.frombuffer(data, dtype=np.int16)
    
    # 3. Atualiza a linha do gráfico
    line.set_ydata(data_np)
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        frame_rate = frame_count / (time.time() - start_time)
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break