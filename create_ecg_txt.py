'''
[Python]
- Signal ECG
- txt
- Plot
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, utilizando el módulo
"pyserial", en este caso el programa se 
encarga de recibir datos con una determinada
trama, se realiza la decodificación de la misma
y se obtienen los valores a graficar en tiempo
real usando el objeto "animation" de matplotlib.
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import os
from scipy.misc import electrocardiogram
import matplotlib.pyplot as plt
import numpy as np

script_path = os.path.dirname(os.path.realpath(__file__))
filename = 'ecg_data.txt'
filename_path = os.path.join(script_path, filename)


def set_frame(float1, float2):
    '''
    Función que recibe los datos
    y crea una trama para luego
    ser enviado por Comunicación
    Serial.
    '''
    str1 = str(float1)
    str2 = str(float2)
    frame = '#' + str1 + ';' + str2 + '#\n'
    return frame 


def set_ecg_to_txt (time, ecg):
    with open(filename_path, 'w') as f:
        # Esto es sólo para guardar una parte
        # de la señal ECG
        time_red_min = np.where(time >= 9)
        time_red_max = np.where(time <= 10.2)
        index_min = time_red_min[0][0]
        index_max = time_red_max[0][-1]

        for (t, y) in zip(time[index_min:index_max + 1], ecg[index_min: index_max + 1]):
            data = set_frame(t, y)
            f.write(data)   # Almaceno la trama con los datos en el .txt
    
    print('El archivo "{}" ha sido creado correctamente.'.format(filename))
    print('Los Datos han sido cargados correctamente.')


def plot_ecg(x, y, label):
    fig = plt.figure()
    
    ax = fig.add_subplot()
    ax.set_xlabel("$[seg]$", fontsize=12)
    ax.set_ylabel("$[mV]$", fontsize=12)
    ax.set_xlim(9, 10.2)
    ax.set_ylim(-1, 1.5)
    ax.plot(x, y, label=label)
    ax.grid()
    
    plt.legend()
    plt.show()


# La señal devuelta es un electrocardiograma (ECG) en mV. de 5 minutos 
# de duración, un registro médico de la actividad eléctrica del 
# corazón, muestreado a 360 Hz.
def create_signal_ecg():
    ecg = electrocardiogram()
    Fs = 360        # Fs: Frecuency Sampling
    Ts = 1 / Fs     # Ts: Periode Sampling
    N = ecg.size    # Cantidad de Muestras.
    t = np.linspace(0, N/Fs, N)     # Vector tiempo.
    return t, ecg


if __name__ == '__main__':
    t, ecg = create_signal_ecg()
    set_ecg_to_txt(time=t, ecg=ecg)
    plot_ecg(x=t, y=ecg, label='ECG Signal')