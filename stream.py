'''
[Python]
- Comunicación Serial
- Receiver
- Stream
- Plot in Real Time
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


import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib import animation as animation
import threading

# Global variables that contains the data extracted and decoded by Tx Serial.
x_data = []
y_data = []

y_lim = ()


#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
ln, = plt.plot(x_data, y_data, color='forestgreen', label='Data Received')
ax.set_xlabel('$t[seg]$', fontsize=13)
ax.set_ylabel('$[mV]$', fontsize=13)
ax.set_facecolor(color='lightyellow')
ax.legend()
ax.grid()


def list_ports():
    '''
    Función que muestra la cantidad
    de puertos disponibles.
    '''
    port_name = ''
    ports = serial.tools.list_ports.comports()
    print('Ports available: ', end='')
    for port in ports:
        port_name += ('"' + port.device + '"' + ', ')      
    print(port_name[:-2])


# Configure/Open Serial instance:
def init_serial():
    '''
    Función que Inicializa/Configura
    un puerto para la posterior comunicación
    serie.
    Retorna la instancia del objeto "serial".
    '''
    ser = serial.Serial()                           # Serial object instance.
    ser.port = 'COM4'                               # set the port name.
    ser.baudrate = 9600                             # set baudrate.
    ser.parity = serial.PARITY_NONE                 # set the parity bit.
    ser.stopbits = serial.STOPBITS_ONE              # set the number of stop bits.
    ser.bytesize = serial.EIGHTBITS                 # set bytesize.
    ser.timeout = 5                                 # set timeout.
    return ser


def open_port(serial_port):
    serial_port.open()      # Open port.
    print('The port "{}" has been opened.'.format(serial_port.portstr))


def close_port(serial_port):
    serial_port.close()
    print('The port "{}" has been closed.'.format(serial_port.portstr))


def is_float(string_num):
    try:
        float(string_num)
        return True
    except ValueError:
        return False


def push_rx(data_rx):
    '''
    Función que recibe una trama
    de datos y verifica que los
    mismos 'válidos' según
    trama, para luego almacenarlos en un
    buffer
    '''
    try:
        if data_rx[0] == '#' and data_rx[-1] == '#':
            pxy = data_rx[1:-1]
            if len(pxy.split(';')) == 2:
                x_s = pxy.split(';')[0]
                y_s = pxy.split(';')[1]
                if is_float(x_s) and is_float(y_s):
                    x_data.append(float(x_s))
                    y_data.append(float(y_s))
                    print(float(x_s), float(y_s))
                else:
                    print('Frame not valid.')
            else:
                print('Frame not valid.')
        else:
            print('Frame not valid.')
    except IndexError:
        print('Frame not received.')


def stream():
    # Inicializamos el puerto serial.
    ser = init_serial() 
    if not ser.is_open:             # ser.is_open is False:
        open_port(ser)

    data_decode = None

    while data_decode != '#FIN#' or data_decode is None:
            data_rx = ser.readline()
            data_decode = data_rx.decode('utf-8').strip()
            if data_decode != '#FIN#':
                push_rx(data_decode)
            else:
                print('End of transmission.') 
    close_port(ser)


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
        ylim = ax.get_ylim()
        fig.canvas.draw()


# Función que actualizará los datos de la gráfica
# Se llama periódicamente desde 'FuncAnimation'.
def update(num, ln):
    init_function()
    ln.set_data(x_data, y_data)
    return ln,


if __name__ == '__main__':
    list_ports()

    ani = animation.FuncAnimation(fig, update, fargs=(ln,),
                interval=50, blit=True)

    # Creamos el hilo y le pasamos la función que va a ejecutar.
    # Luego iniciamos el hilo.
    data_collector = threading.Thread(target=stream)
    data_collector.start()
    
    # Mostramos la figura y el axis.
    plt.show()
    
    data_collector.join()
