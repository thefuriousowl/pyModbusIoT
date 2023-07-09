import struct

# SLAVE/MASTER READ DEFINITION
class ModbusReadDefinitionParam:
    def __init__(self, SLAVE_ID=1, START_ADDRESS=1, COUNT=1, FUNCTION_CODE=3):
        self.SLAVE_ID = SLAVE_ID
        self.START_ADDRESS = START_ADDRESS
        self.COUNT = COUNT
        self.FUNCTION_CODE = FUNCTION_CODE


class ModbusReader:
    def __init__(self, reader=None):
        self.reader = reader
        self.reg_buffer = None
        self.bits_buffer = None
        self.modbus_output = None

    def read_registers(self, slave_id=1, start_address=1, count=1, fn_code=3):
        if (fn_code == 4): response = self.reader.read_input_registers(address=start_address, count=count, slave=slave_id)
        elif (fn_code == 3): response = self.reader.read_holding_registers(address=start_address, count=count, slave=slave_id)
        else:
            print("Invalid Function Code: ", fn_code)
            self.reg_buffer = -1
        if response.isError():
            print("Error reading registers: ", response)
            self.reg_buffer = -1
        else:
            response_buffer = []
            for res in response.registers:
                response_buffer.append(res)

            self.reg_buffer = response_buffer
            self.modbus_output = response_buffer

    def read_discrete(self, slave_id=1, start_address=1, count=1, fn_code=1):
        if (fn_code == 1): response = self.reader.read_coils(address=start_address, count=count, slave=slave_id)
        elif (fn_code == 2): response = self.reader.read_discrete_inputs(address=start_address, count=count, slave=slave_id)
        else:
            print("Invalid Function Code: ", fn_code)
            self.bits_buffer = -1
        if response.isError():
            print("Error reading registers: ", response)
            self.bits_buffer = -1
        else:
            response_buffer = []
            for res in response.bits:
                response_buffer.append(res)

            self.bits_buffer = response_buffer
            self.modbus_output = response_buffer


    def get_float32(self, byte_swap=True, byte_order="big"):

        if (self.reg_buffer is None or self.reg_buffer == -1): print("Invalid reg_buffer: ", self.reg_buffer)
        else:
            raw_value = (self.reg_buffer[0] << 16) + self.reg_buffer[1]

            # Convert the integer value to bytes in the specified byte order.
            if byte_swap:
                raw_value = ((raw_value & 0xFF00FF00) >> 8) | ((raw_value & 0x00FF00FF) << 8)

            if byte_order == "big":
                value_bytes = raw_value.to_bytes(4, byteorder='big')
            elif byte_order == 'little':
                value_bytes = raw_value.to_bytes(4, byteorder='little')
            else:
                print("Invalid byte order: ", byte_order)

            # Unpack the bytes as a float32 value
            float_value = struct.unpack('!f', value_bytes)[0]

            self.modbus_output = float_value
        
    def get_int16(self):
        if (self.reg_buffer is None or self.reg_buffer == -1): print("Invalid reg_buffer: ", self.reg_buffer)
        else:
            int_value = self.reg_buffer[0]
            if int_value >= 32768: # Check if value is negative.
                int_value -= 65536 # Convert to signed integer.

            self.modbus_output = int_value
    
    def get_int32(self):
        if (self.reg_buffer is None or self.reg_buffer == -1): print("Invalid reg_buffer: ", self.reg_buffer)
        else:
            int_value = (self.reg_buffer[0] << 16) + self.reg_buffer[1]
            if int_value >= 2147483648: # Check if value is negative.
                int_value -= 4294967296   # Convert to signed integer.

            self.modbus_output = int_value
        