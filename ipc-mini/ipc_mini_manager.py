import socket

class IPCMiniManager:

    def __init__(self, ip, port=23, timeout=1):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.s = socket.create_connection((self.ip, self.port), self.timeout)

    def __del__(self):
        print(f'IPC Mini Manager for {self.ip} closed.')
        self.s.close()

    def get_pressure(self):
        '''
        Reads pressure from the IPC Mini.
        
        Returns:
            float: The pressure value.
            int: -1 if there is an error.
        '''
        message = b'\x02\x808120\x0388'
        try:
            self.s.sendall(message)
            response = self.s.recv(1024)
            response = float(response[6:14])
        except Exception as e:
            print(e)
            return -1
        return response

    def get_current(self):
        '''
        Reads measured current from the IPC Mini.
        
        Returns:
            float: The current value.
            int: -1 if there is an error.
        '''
        message = b'\x02\x808110\x038B'
        try:
            self.s.sendall(message)
            response = self.s.recv(1024)
            response = float(response[6:14])
        except Exception as e:
            print(e)
            return -1
        return response

    def get_voltage(self):
        '''
        Reads mreasured voltage from the IPC Mini.
        
        Returns:
            float: The voltage value.
            int: -1 if there is an error.
        '''
        message = b'\x02\x808100\x038A'
        try:
            self.s.sendall(message)
            response = self.s.recv(1024)
            response = float(response[6:12])
        except Exception as e:
            print(e)
            return -1
        return response

    def _generate_message(WIN1, WIN2, WIN3, COM):
        '''
        Generate message to send to the IPC Mini. The meanings of WIN and COM are outlined the manual.

        Example: for pressure (window=812) WIN1=0x38, WIN2=0x31, WIN3=0x32, COM=0x30
        811 = measured current
        810 = measured voltage
        '''
        STX = 0x02
        ADDR = 0x80
        COM = 0x30
        ETX = 0x03

        # Calculate checksum
        CRCraw = ADDR ^ WIN1 ^ WIN2 ^ WIN3 ^ COM ^ ETX  # XOR calculation
        CRC1 = (CRCraw >> 4) & 0x0F  # High nibble
        CRC2 = CRCraw & 0x0F         # Low nibble

        # Convert nibbles to ASCII
        def nibble_to_ascii(nibble):
            if nibble < 10:
                return nibble + 0x30  # ASCII for '0'–'9'
            else:
                return nibble + 0x37  # ASCII for 'A'–'F'

        CRC1_ascii = nibble_to_ascii(CRC1)
        CRC2_ascii = nibble_to_ascii(CRC2)

        # Construct the command
        command = [STX, ADDR, WIN1, WIN2, WIN3, COM, ETX, CRC1_ascii, CRC2_ascii]

        # Convert to byte string
        tobesent = bytes(command)

        # Print results
        a = ' '.join(hex(c) for c in command)
        print(a)         # Hexadecimal representation
        print(tobesent)  # Final byte string to be sent