'''
[Python]
- Comunicación Serial
- Transmitter
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, utilizando el módulo
"pyserial", en este caso el programa se 
encarga de transmitir datos con una determinada
trama.
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import serial


# Global variable that contains the data transmited by Tx Serial.
buff_tx = ['#12;18#', '#25;47#', '#47;59#', '#0;96#',
            '#44;66#', '#55;98#', '#5;0#', '#23;32#']    


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


def pop_tx(index):
    '''
    Función que toma un dato
    del buffer y lo retorna,
    según el índice pasado
    como argumento.
    '''
    frame = buff_tx[index]
    frame = frame + '\n'
    data_tx = frame.encode()

    return data_tx


def transmitter(data_tx):
    '''
    Función que verifica si el
    puerto en cuestión puede ser
    abierto, en caso afirmativo,
    crea un ciclo para transmitir
    cada dato de un buffer a través
    de comunicación serial.
    '''
    ser = init_serial()
    print('Connected to port: "{}"'.format(ser.portstr))
    
    if not ser.is_open:             # ser.is_open is False:
        try:
            ser.open()  # Open port.
            print('The port "{}" has been opened.'.format(ser.portstr))
            #ser.timeout = None      # 'None' if you want "readline()" to be blocking.

            for i in range(len(buff_tx)):
                data_tx = pop_tx(i)
                ser.write(data_tx)
                
            ser.close()
            print('The port has been closed.')

        except serial.serialutil.SerialException:
            print('Could not open port "{}".'.format(ser.portstr))


if __name__ == '__main__':
    transmitter(buff_tx)
