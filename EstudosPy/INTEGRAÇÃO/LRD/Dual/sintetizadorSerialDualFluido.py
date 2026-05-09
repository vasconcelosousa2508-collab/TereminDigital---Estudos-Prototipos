import serial
import numpy as np
import sounddevice as sd
from pynput import keyboard

#config
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