'''
[Python]
- Comunicación Serial
- Receiver
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, utilizando el módulo
"pyserial", en este caso el programa se 
encarga de recibir datos con una determinada
trama.
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import serial
import serial.tools.list_ports

buff_rx = []    # Global variable that contains the data extracted by Tx Serial.


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


def push_rx(data_rx):
    '''
    Función que recibe una trama
    de datos y verifica que los
    mismos 'válidos' según
    trama, para luego almacenarlos en un
    buffer
    '''
    if data_rx[0] == '#' and data_rx[-1] == '#':
        pxy = data_rx[1:-1]
        if len(pxy.split(';')) == 2:
            x_s = pxy.split(';')[0]
            y_s = pxy.split(';')[1]
            if x_s.isdigit() and y_s.isdigit():
                print(x_s, y_s)
                buff_rx.append([int(x_s), int(y_s)])
            else:
                print('Frame not valid.')
        else:
            print('Frame not valid.')
    else:
        print('Frame not valid.')


def receiver():
    '''
    Función que verifica si el
    puerto en cuestión puede ser
    abierto, en caso afirmativo,
    crea un bucle infinito donde
    se recibe cada dato llegado
    por comunicación serial.
    Retorna el buff_rx con los datos
    importantes.
    '''
    ser = init_serial()
    print('Connected to port: "{}"'.format(ser.portstr))
    
    if not ser.is_open:             # ser.is_open is False:
        try:
            ser.open()  # Open port.
            print('The port "{}" has been opened.'.format(ser.portstr))
            #ser.timeout = None      # 'None' if you want "readline()" to be blocking.

            while True:
                try:
                    msgframe = ser.readline()
                    msg_decode = msgframe.decode('utf-8').strip()
                    if msg_decode != '':
                        push_rx(msg_decode)
                    else:
                        print('Frame not received.')
                    
                except KeyboardInterrupt:
                    ser.close()
                    print('The port has been closed.')
                    return buff_rx

        except serial.serialutil.SerialException:
            print('Could not open port "{}".'.format(ser.portstr))


if __name__ == '__main__':
    list_ports()
    receiver()
    print(buff_rx)

