import serial
import io
from matplotlib import pyplot as plt

# Configure/Open Serial instance:
def init_serial():
    ser = serial.Serial()                           # Serial object instance.
    ser.port = 'COM4'                               # set the port name.
    ser.baudrate = 9600                             # set baudrate.
    ser.parity = serial.PARITY_NONE                 # set the parity bit.
    ser.stopbits = serial.STOPBITS_ONE              # set the number of stop bits.
    ser.bytesize = serial.EIGHTBITS                 # set bytesize.
    ser.timeout = 5                                 # set timeout.

    return ser


def receiver():
    ser = init_serial()
    buff_Rx = []
    print('Connected to: {}'.format(ser.portstr))
    
    if not ser.is_open:             # ser.is_open is False:
        ser.open()  # Open port.
        print('The port has been opened.')
        #ser.timeout = None      # If you want "readline()" to be blocking.
    else:
        print('The port is closed.')

    msgframe = ser.readline()
    while True:
        msg_decode = msgframe.decode('utf-8').strip()
        if msg_decode != '':
            if msg_decode[0] == '#' and msg_decode[-1] == '#':
                point = msg_decode[1:-1]
                if len(point.split(';')) == 2:
                    x_s = point.split(';')[0]
                    y_s = point.split(';')[1]
                    if x_s.isdigit() and y_s.isdigit():
                        x = int(x_s)
                        y = int(y_s)
                        buff_Rx.append([x, y])
                        print(x, y)
                    else:
                        break
        
        msgframe = ser.readline()

    ser.close()
    print('The port has been closed.')
    return buff_Rx


if __name__ == '__main__':
    buff_Rx = receiver()
    print(buff_Rx)

