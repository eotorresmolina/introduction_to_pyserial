import serial
import io
from matplotlib import pyplot as plt

buff_rx = []    # Global variable that contains the data extracted by Tx Serial.

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


def push_rx(frame_d):
    if frame_d[0] == '#' and frame_d[-1] == '#':
        pxy = frame_d[1:-1]
        if len(pxy.split(';')) == 2:
            x_s = pxy.split(';')[0]
            y_s = pxy.split(';')[1]
            if x_s.isdigit() and y_s.isdigit():
                buff_rx.append([int(x_s), int(y_s)])
            else:
                print('Frame not valid.')
        else:
            print('Frame not valid.')
    else:
        print('Frame not valid.')


def receiver():
    ser = init_serial()
    buff_Rx = []
    print('Connected to: {}'.format(ser.portstr))
    
    if not ser.is_open:             # ser.is_open is False:
        ser.open()  # Open port.
        print('The port has been opened.')
        #ser.timeout = None      # 'None' if you want "readline()" to be blocking.
    else:
        print('The port is closed.')

    while True:
        msgframe = ser.readline()
        msg_decode = msgframe.decode('utf-8').strip()
        if msg_decode != '':
            push_rx(msg_decode)
        else:
            print('Frame not received.')
            

    ser.close()
    print('The port has been closed.')
    return buff_Rx


if __name__ == '__main__':
    print(buff_rx)

