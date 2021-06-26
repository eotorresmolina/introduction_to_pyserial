'''
[Python]
- Comunicación Serial
- Class Stream
- Receiver
- Transmitter
---------------------------
Autor: Torres Molina Emmanuel O.
Version: 1.1
Descripción:
Pequeño ejemplo de introducción a la 
comunicación serial, utilizando el módulo
"pyserial", en este caso se crea una clase
"Stream" compuesta de un objeto "serial"
para la configuración de un puerto, la transmisión
y recepción de una determinada trama.
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt


class Stream():
    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        super(Stream, self).__init__()   # Equivale a: super().__init__()
        self.ser = serial.Serial()
        self.buff_tx = ['#0;1#','#1;2#', '#2;4#', '#3;8#', '#4;16#', '#5;32#']
        self.buff_rx = []
        self.x = []
        self.y = []
        self.y_lim = ()
        self.init_serial(port, baudrate, parity, stopbits, bytesize, timeout)
    
    def init_serial(self, port, baudrate, parity, stopbits, bytesize, timeout):
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.bytesize = bytesize
        self.ser.timeout = timeout


    def list_ports(self,):
        '''
        Función que muestra la cantidad
        de puertos disponibles.
        '''
        port_name = ''
        puertos = serial.tools.list_ports.comports()
        print('Ports available: ', end='')
        for p in puertos:
            port_name += ('"' + p.device + '"' + ', ')      
        print(port_name[:-2])

    def open_port(self,):
        try:
            self.ser.open()      # Open port.
            print('The port "{}" has been opened.'.format(self.ser.portstr))
        except serial.serialutil.SerialException:
            print('Could not open port "{}".'.format(self.ser.portstr))

    def close_port(self,):
        self.ser.close()
        print('The port "{}" has been closed.'.format(self.ser.portstr))

    def pop_tx(self, index):
        data = self.buff_tx[index]
        data = data + '\n'
        data_tx = data.encode()
        return data_tx

    def transmitter(self,):
        if self.buff_tx != []:
            for data in range(len(self.buff_tx)):
                msg = self.pop_tx(data)
                self.ser.write(msg)

    def set_values(self, msg):
        try:
            if msg[0] == '#' and msg[-1] == '#':
                data = msg[1:-1]
                pxy_s = data.split(';')
                px_s = pxy_s[0]
                py_s = pxy_s[1]
                if self.is_float(px_s) and self.is_float(py_s):
                    self.x.append(float(px_s))
                    self.y.append(float(py_s))
        except IndexError:
            pass

    def push_rx(self, msg):
        try:
            if msg[0] == '#' and msg[-1] == '#':
                data = msg[1:-1]
                pxy_s = data.split(';')
                px_s = pxy_s[0]
                py_s = pxy_s[1]
                if self.is_float(px_s) and self.is_float(py_s):
                    self.buff_rx.append(msg)
                    print('Frame received: {}' .format(msg))
                else:
                    print('Frame not valid.')
        except IndexError:
            print('Frame not received.')

    def receiver(self,):
        msg_decoded = None
        while msg_decoded != '#FIN#' or msg_decoded is None:
            frame = self.ser.readline()
            msg_decoded = frame.decode('utf-8').strip()
            if msg_decoded != '#FIN#':
                self.push_rx(msg_decoded)
                self.set_values(msg_decoded)
            else:
                print('End of transmission.') 

    def is_float(self, my_string):
        try:
            float(my_string)
            return True
        except:
            return False


    def setup_figure(self,):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ln, = plt.plot(self.x, self.y, color='forestgreen', label='Data Received')
        self.ax.set_xlabel('$t[seg]$', fontsize=13)
        self.ax.set_ylabel('$[mV]$', fontsize=13)
        self.ax.set_facecolor(color='lightyellow')
        self.ax.legend()
        self.ax.grid()