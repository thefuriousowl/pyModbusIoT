import subprocess
from flask import Flask, request, jsonify
import sys
import psycopg2
from modules.ModbusConnection import ModbusMaster, ModbusClient, ModbusRtuConnectionParam, ModbusTcpConnectionParam
from modules.ModbusReader import ModbusReader, ModbusReadDefinitionParam
from modules.MQTTBroker import MQTTBroker, MqttBrokerConnectionParam
import time
import yaml

def load_yaml(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            eprint("YAML Config has been sucessfully loaded!: ", data)
        return data
    except Exception as e:
        eprint("Failed to load YAML file: ", str(e))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


app = Flask(__name__)
    
# INITIALIZE PARAMETER

CURRENT_MODBUS_RTU_PARAM = ModbusRtuConnectionParam()
CURRENT_MODBUS_TCP_PARAM = ModbusTcpConnectionParam()
CURRENT_MODBUS_READER_PARAM = ModbusReadDefinitionParam()
CURRENT_MQTT_BROKER_PARAM = MqttBrokerConnectionParam()


@app.route("/modbus_rtu_connection_conf", methods=['POST'])
def modbus_rtu_connection_conf_post():
    global CURRENT_MODBUS_RTU_PARAM
    data = request.get_json()
    CURRENT_MODBUS_RTU_PARAM = ModbusRtuConnectionParam(**data)
    return jsonify({"MODBUS_RTU_PARAM has been updated with user value": CURRENT_MODBUS_RTU_PARAM.__dict__})

@app.route("/modbus_rtu_connection_conf", methods=['GET'])
def modbus_rtu_connection_conf_get():
    return jsonify(CURRENT_MODBUS_RTU_PARAM.__dict__)

@app.route("/modbus_tcp_connection_conf", methods=['POST'])
def modbus_tcp_connection_conf_post():
    global CURRENT_MODBUS_TCP_PARAM
    data = request.get_json()
    CURRENT_MODBUS_TCP_PARAM = ModbusTcpConnectionParam(**data)
    return jsonify({"MODBUS_RTU_PARAM has been updated with user value": CURRENT_MODBUS_TCP_PARAM.__dict__})

@app.route("/modbus_tcp_connection_conf", methods=['GET'])
def modbus_tcp_connection_conf_get():
    return jsonify(CURRENT_MODBUS_TCP_PARAM.__dict__)

@app.route("/modbus_read_definition_conf", methods=['POST'])
def modbus_read_definition_conf_post():
    global CURRENT_MODBUS_READER_PARAM
    data = request.get_json()
    CURRENT_MODBUS_READER_PARAM = ModbusReadDefinitionParam(**data)
    return jsonify({"MODBUS_READER_PARAM has been update with user value": CURRENT_MODBUS_READER_PARAM.__dict__})

@app.route("/modbus_read_definition_conf", methods=['GET'])
def modbus_read_definition_conf_get():
    return jsonify(CURRENT_MODBUS_READER_PARAM.__dict__)


@app.route("/rtu_read_register", methods=['GET'])
def rtu_read_register():
    output_dict = {}
    global CURRENT_MODBUS_READER_PARAM
    cli = ModbusMaster(com_port=CURRENT_MODBUS_RTU_PARAM["COM_PORT"],
                          stop_bits=CURRENT_MODBUS_RTU_PARAM["STOP_BITS"],
                          byte_size=CURRENT_MODBUS_RTU_PARAM["BYTE_SIZE"],
                          parity=CURRENT_MODBUS_RTU_PARAM["PARITY"],
                          baud_rate=CURRENT_MODBUS_RTU_PARAM["BAUD_RATE"],
                          timeout=CURRENT_MODBUS_RTU_PARAM["TIMEOUT"],
                          strict=False)
    
    cli.connect_to_slave()
    reader = ModbusReader(reader=cli)
    reader.read_registers(slave_id=CURRENT_MODBUS_READER_PARAM["SLAVE_ID"], 
                          start_address=CURRENT_MODBUS_READER_PARAM["START_ADDRESS"],
                          count=CURRENT_MODBUS_READER_PARAM["COUNT"], 
                          fn_code=CURRENT_MODBUS_READER_PARAM["FUNCTION_CODE"])
    output_dict.update({"Holding_Register": reader.get_int16})

    return jsonify(output_dict)
    
@app.route("/tcp_read_register", methods=['GET'])
def tcp_read_register():
    output_dict = {}
    global CURRENT_MODBUS_READER_PARAM
    cli = ModbusClient(host=CURRENT_MODBUS_TCP_PARAM.__dict__["HOST"], port=CURRENT_MODBUS_TCP_PARAM.__dict__["PORT"])
    cli.connect_to_server()
    reader = ModbusReader(reader=cli.cli)
    reader.read_registers(slave_id=CURRENT_MODBUS_READER_PARAM.__dict__["SLAVE_ID"], 
                          start_address=CURRENT_MODBUS_READER_PARAM.__dict__["START_ADDRESS"],
                          count=CURRENT_MODBUS_READER_PARAM.__dict__["COUNT"], 
                          fn_code=CURRENT_MODBUS_READER_PARAM.__dict__["FUNCTION_CODE"])
    reader.get_int32()
    output_dict.update({"Holding_Register": reader.modbus_output})

    return jsonify(output_dict)


@app.route("/tcp_start", methods=['POST'])
def tcp_start():
    global CURRENT_MODBUS_READER_PARAM
    reg_config = load_yaml("reg_config.yaml")

    cli = ModbusClient(host=CURRENT_MODBUS_TCP_PARAM.__dict__["HOST"], port=CURRENT_MODBUS_TCP_PARAM.__dict__["PORT"])
    cli.connect_to_server()
    reader = ModbusReader(reader=cli.cli)


    output_dict = {}
    for k, v in reg_config.items():
        slave_id, reg_address, data_type, byte_order, byte_swap, fn_code = reg_config[k][0], reg_config[k][1], reg_config[k][2], reg_config[k][3], reg_config[k][4], reg_config[k][5]
        if (data_type[-2:] == "16"): address_count = 1
        elif (data_type[-2:] == "32"): address_count = 2
        else: address_count = 1
        if fn_code in [3,4]:
            reader.read_registers(slave_id=slave_id, 
                                        start_address=reg_address,
                                        count=address_count, 
                                        fn_code=fn_code)
            eprint(f"This is reg_buffer address {reg_address}: ", reader.reg_buffer)
            if (data_type == "int16"): reader.get_int16()
            elif (data_type == "float32"): reader.get_float32(byte_swap=byte_swap_to_bool(byte_swap), byte_order=byte_order)
            eprint(reader.modbus_output)
        output_dict.update({k: reader.modbus_output})

    return jsonify(output_dict)

@app.route("/rtu_start", methods=['POST'])
def rtu_start():
    global CURRENT_MODBUS_READER_PARAM
    reg_config = load_yaml("reg_config.yaml")

    master = ModbusMaster(com_port=CURRENT_MODBUS_RTU_PARAM.__dict__["COM_PORT"], 
                          stop_bits=CURRENT_MODBUS_RTU_PARAM.__dict__["STOP_BITS"],
                          byte_size=CURRENT_MODBUS_RTU_PARAM.__dict__["BYTE_SIZE"],
                          parity=CURRENT_MODBUS_RTU_PARAM.__dict__["PARITY"],
                          baud_rate=CURRENT_MODBUS_RTU_PARAM.__dict__["BAUD_RATE"],
                          timeout=CURRENT_MODBUS_RTU_PARAM.__dict__["TIMEOUT"])
    master.connect_to_slave()
    reader = ModbusReader(reader=master.cli)

    output_dict = {}
    for k, v in reg_config.items():
        slave_id, reg_address, data_type, byte_order, byte_swap, fn_code = reg_config[k][0], reg_config[k][1], reg_config[k][2], reg_config[k][3], reg_config[k][4], reg_config[k][5]
        if (data_type[-2:] == "16"): address_count = 1
        elif (data_type[-2:] == "32"): address_count = 2
        else: address_count = 1
        if fn_code in [3,4]:
            reader.read_registers(slave_id=slave_id, 
                                        start_address=reg_address,
                                        count=address_count, 
                                        fn_code=fn_code)
            eprint(f"This is reg_buffer address {reg_address}: ", reader.reg_buffer)
            if (data_type == "int16"): reader.get_int16()
            elif (data_type == "float32"): reader.get_float32(byte_swap=byte_swap_to_bool(byte_swap), byte_order=byte_order)
            eprint(reader.modbus_output)
        output_dict.update({k: reader.modbus_output})

    return jsonify(output_dict)




def byte_swap_to_bool(str):
    if (str == "byte-swap"): return True
    else: return False