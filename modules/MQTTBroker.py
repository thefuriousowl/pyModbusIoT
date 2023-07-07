import paho.mqtt.client as mqtt

class MqttBrokerConnectionParam:
    def __init__(self, BROKER_IP = "45.136.255.134", BROKER_PORT=1883):
        self.BROKER_IP = BROKER_IP
        self.BROKER_PORT = BROKER_PORT

class MQTTBroker:
    def __init__(self, host= "45.136.255.134", port=1883, topic=""):
        self.cli = mqtt.Client()
        self.host = host
        self.port = port
        self.topic = topic

    def connect_to_broker(self):
        self.cli.connect(host=self.host, port=self.port)


    def publish_test(self):
        self.cli.publish(self.topic, "MQTT message has been sent from CLI.")
