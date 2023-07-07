# Modbus2Mqtt
Communicate with Modbus Protocol and send out the value via mqtt.
Support Modbus Function code 1,2,3,4 for now.

# Prerequisite
- Docker engine
- Docker compose plugin

# Usage
  1. Start the container by using command: 'docker compose up --build'. Specify -d argument will force container to run in background process.
  2. MODBUS RTU Master

     2.1  GET: {URL}/modbus_rtu_config. To see the current parameter of MODBUS_RTU_PARAM
     2.2  POST: {URL}/modbus_rtu_config. To update the current parameter of MODBUS_RTU_PARAM. MODBUS_RTU_PARAM must contain these parameter:
     
     	  {
     			"MODBUS_RTU_PARAM": 
     			{
     				"START_ADDRESS": 101,
					"MODBUS_RANGE": 1,
     				"SLAVE_ID": 1,
     				"COM_PORT": "/dev/ttyUSB0",
     				"STOP_BITS": 1,
    				"BYTE_SIZE": 8,
    				"PARITY": "N",
   					"BAUD_RATE": 9600,
					"FUNCTION_CODE": 3,
   					"TIMEOUT": 1
 					}
				}
		
	 	2.3 GET: {URL}/start_rtu_master. To start MODBUS_RTU_MASTER to read register from specified slave.
     
  3. MODBUS TCP Client
     
     3.1  GET: {URL}/modbus_tcp_config. To see the current parameter of MODBUS_TCP_PARAM
     
     3.2	POST: {URL}/modbus_rtu_config. To update the current parameter of MODBUS_RTU_PARAM. To update via request body, MODBUS_RTU_PARAM must contain these parameter:
     
     		{
  				"MODBUS_TCP_PARAM": 
 					{
    				"MODBUS_HOST": "192.168.2.127",
    				"START_ADDRESS": 1,
    				"MODBUS_RANGE": 5,
					"FUNCTION_CODE": 3,
    				"NODE_ID": 1
 					}
				}

		3.3 GET: {URL}/start_tcp_client. To start MODBUS_TCP_CLIENT to read register from specified Modbus server node.

  4. MQTT Broker

		4.1 GET: {URL}/mqtt_broker_config. To see the current parameter of MQTT_BROKER_PARAM.

		4.2 POST: {URL}/mqtt_broker_config. To update the current parameter of MQTT_BROKER_PARAM. To update via request body, MQTT_BROKER_PARAM must contain these parameter:
     
			{
    		"BROKER_IP": "45.136.255.134",
    		"BROKER_PORT": 1884
			}

  5. Stop all current process running

     -	POST: {URL}/stop_all

			
