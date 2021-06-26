'''
[Python]
- Comunicación Serial
- Test Bench
- OOP
- Transmitter
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, se instancia un objeto
de la clase "Stream" y se procede a enviar una
determinada "trama" llamando al método "transmitter".
Formato de la trama: '#x;y#'
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"

import serial
from oop_stream import Stream


if __name__ == '__main__':
    strm = Stream(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, 
                    stopbits=1, bytesize=8, timeout=5)
    strm.list_ports()
    strm.open_port()
    strm.close_port()