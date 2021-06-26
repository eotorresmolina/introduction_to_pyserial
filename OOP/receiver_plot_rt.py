'''
[Python]
- Comunicación Serial
- Test Bench
- OOP
- Receiver
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, se define una clase
"StreamTX" que deriva de la clase "Stream", 
se redefine el método "receiver" para que se 
adapte a una trama en formato JSON, así, 
decodifica los valores y realiza un gráfico 
en tiempo real de los datos recibidos.

NOTA: Para enviar los datos se utilzó el
software "RealTerm".
'''

from oop_stream import Stream
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import threading
import serial
import json


# Global variables that contains the data extracted and decoded by Tx Serial.
x_data = []
y_data = []

y_lim = ()


#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
ln, = plt.plot(x_data, y_data, color='darkred', label='Data Received')
ax.set_xlabel('$t[seg]$', fontsize=13)
ax.set_ylabel('$[mV]$', fontsize=13)
ax.set_facecolor(color='lightyellow')
ax.legend()
ax.grid()


class StreamTX (Stream):
    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        super().__init__(port=port, baudrate=baudrate, parity=parity, 
                    stopbits=stopbits, bytesize=bytesize, timeout=timeout)
        self.list_ports()
        self.open_port()

    def push_rx(self, data_rx):
        '''
        Función que recibe una trama
        de datos y verifica que los
        mismos sean 'válidos' según la
        trama, para luego almacenarlos en
        2 listas.
        '''
        try:
            json_data = json.loads(data_rx)
            d_values = json_data.values()
            values = [x for x in d_values]
            x_s = values[0]
            y_s = values[1]
            if self.is_float(x_s) and self.is_float(y_s):
                x_data.append(float(x_s))
                y_data.append(float(y_s))
                print('Frame received: {}' .format(data_rx))
            else:
                print('Frame not valid.')
        except json.decoder.JSONDecodeError:
            print('Frame not valid.')

    def stream(self,):
        data_decode = None
        while data_decode != '#FIN#' or data_decode is None:
            data_rx = self.ser.readline()
            if data_rx != '':
                data_decode = data_rx.decode('utf-8').strip()
                if data_decode != '#FIN#':
                    self.push_rx(data_decode)
                else:
                    print('End of transmission.')
            else:
                print('Frame not received.')

    def __del__(self,):
        self.close_port()


def init_function():
    # Permite auto-ajustar el eje de las Y en 
    # función del contenido de la gráfica.
    ax.relim()
    ax.autoscale_view()
    
    # Ahora monitoreamos los valores del límite del eje Y 
    # para detectar cuando la gráfica ha sido reajustada. 
    # Es decir, redibuja las etiquetas del eje Y a medida 
    # que se reajusta. Si no, las etiquetas permanecen mientras
    # el eje se reajusta (los valores no coinciden con lo
    # desplegado en el eje). 
    global y_lim
    if ax.get_ylim() != y_lim:
        y_lim = ax.get_ylim()
        fig.canvas.draw()


# Función que actualizará los datos de la gráfica
# Se llama periódicamente desde 'FuncAnimation'.
def update(num, ln):
    init_function()
    ln.set_data(x_data, y_data)
    return ln,


if __name__ == '__main__':
    tx = StreamTX(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=5)
        
    ani = animation.FuncAnimation(fig, update, fargs=(ln,),
        interval=50, blit=True)

    # Creamos el hilo y le pasamos la función que va a ejecutar.
    # Luego iniciamos el hilo.
    data_collector = threading.Thread(target=tx.stream)
    data_collector.start()
    
    # Mostramos la figura y el axis.
    plt.show()

    data_collector.join()