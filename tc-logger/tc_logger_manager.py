import serial
import re
import time

class TCLogger:
    
    def __init__(self, port='COM0'):
        '''
        Configures the serial connection to the thermocouple logger. Hardware by Jim MacArthur.

        Channels 0-23: thermocouple reader
        Channels 24-25: AO Sense window and heater respectively
        Channels 26-27: alias of 24-25 for misc. reasons
        
        Communication with the hardware is via RS-485 serial. Commands are terminated by ';'. Sucessfully executed commmands are appended by '!' in the response.
        'C{n};': set the channel to n
        't;': read the temperature of the currently set channel

        Params:
        Port: port of the logger (to find the port, open Windows Device Manager and navigate to "Ports")

        Example:
        tclogger = TCLogger('COM7')
        print(tclogger.read_channel(0))
        print(tclogger.read_channel(1))
        tclogger.close()
        '''
        self.ser = serial.Serial(port=port, timeout=0.05)
        if self.ser.is_open:
            print(f'Established connection to TC Logger at {port}')

    def _write(self, data):
        '''
        Write via serial
        '''
        try:
            self.ser.write(data.encode('utf-8'))
        except Exception:
            self.ser.close()

    def _read(self):
        '''
        Read 10 bytes via serial
        '''
        try:
            # give the thermocouple reader 50 ms to respond
            time.sleep(0.05)
            data = b""
            while self.ser.in_waiting > 0:
                chunk = self.ser.read(self.ser.in_waiting)  # Read all available bytes
            data += chunk  # Append the received chunk to the existing data
            return data.decode('utf-8')
        except Exception:
            self.ser.close()
        
    def read_channel(self, chan):
        '''
        Read the temperature of a channel

        Parameters:
        chan: channel number (starts from 0)

        Returns: temperature in C or None if channel can not be read
        '''
        self._write(f'C{chan};t;')
        resp = self._read()

        temp = re.search(r"t\d+!", resp)
        if temp:
            return float(temp.group(0)[1:-1])/100
        return None

    def close(self):
        '''
        Closes the serial connection to the hardware.
        '''
        self.ser.close()