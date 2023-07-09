import paho.mqtt.client as mqtt
import socket

class MqttBrokerConnectionParam:
    def __init__(self, BROKER_IP = "45.136.255.134", BROKER_PORT=1883, INTERVAL=10, TOPIC="Modbus2Mqtt/Test"):
        self.BROKER_IP = BROKER_IP
        self.BROKER_PORT = BROKER_PORT
        self.INTERVAL = INTERVAL
        self.TOPIC = TOPIC

class MQTTBroker:
    def __init__(self, host= "45.136.255.134", port=1883, topic=""):
        self.cli = mqtt.Client()
        self.host = host
        self.port = port
        self.topic = topic

    def connect_to_broker(self):
        self.cli.connect(host=self.host, port=self.port)


    def publish_message(self, message):
        self.cli.publish(self.topic, message)


class UdpConnectionParam:
    def __init__(self, SERVER_IP = "45.136.255.134", PORT=55555, INTERVAL=10):
        self.SERVER_IP = SERVER_IP
        self.PORT = PORT
        self.INTERVAL = INTERVAL

class Udp:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port

    def send_via_udp(self, message):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send a message
        sock.sendto(message.encode(), (self.server_ip, self.port))
        # Close the socket
        sock.close()