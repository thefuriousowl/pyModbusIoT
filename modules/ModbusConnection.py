from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusTcpClient
import time
import sys
import requests

# MODBUS RTU PARAMETER
class ModbusRtuConnectionParam:
    def __init__(self, COM_PORT="/dev/ttyUSB0", STOP_BITS=1,
                 BYTE_SIZE=8, PARITY='N', BAUD_RATE=9600, TIMEOUT=1):
        self.COM_PORT = COM_PORT
        self.STOP_BITS = STOP_BITS
        self.BYTE_SIZE = BYTE_SIZE
        self.PARITY = PARITY
        self.BAUD_RATE = BAUD_RATE
        self.TIMEOUT = TIMEOUT


# MODBUS TCP/IP PARAMETER
class ModbusTcpConnectionParam:
    def __init__(self, HOST= '192.168.2.127', PORT=502):
        self.HOST = HOST
        self.PORT = PORT

        
class ModbusMaster:
    def __init__(self, com_port="/dev/ttyUSB0", 
                 stop_bits=1, byte_size=8, 
                 parity='N', baud_rate=9600, timeout=1):
        
        self.com_port = com_port
        self.stop_bits = stop_bits
        self.byte_size = byte_size
        self.parity = parity
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.cli = None

    def connect_to_slave(self):
        self.cli = ModbusSerialClient(port=self.com_port, stopbits=self.stop_bits,
                                                bytesize=self.byte_size, parity=self.parity,
                                                baudrate=self.baud_rate, timeout=self.timeout, strict=False)
        self.cli.connect()
        

class ModbusClient:
    def __init__(self, host= 'localhost', port= 502):
        self.host = host
        self.port = port
        self.cli = None
        

    def connect_to_server(self):
        self.cli = ModbusTcpClient(host=self.host, port=self.port)
        self.cli.connect()


