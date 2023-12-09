import paho.mqtt.client as mqtt
import json
from time import sleep
import time
from Group8_COMP216_Lab6_Data_Generator import *
import uuid

class Publisher:
    def __init__(self, delay=1, topic='COMP216'):
        self.util = DataGenerator(data_range=(200, 1100))
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        try:
            self.client.connect('localhost', 1883)
        except mqtt.MQTTException as e:
            print(f'MQTT Exception: {e}')



    def publish(self, times=1):
        for x in range(times):
            if random.randint(1, 100) == 1:
                print("\nSkipping transmission.")
                continue
            print(f'\n#{x}\n', end=' ')
            self.__publish()
    
   
    def generate_packet_id(self):
            packet_id = str(uuid.uuid4())
            return packet_id

    def __publish(self):
        data = self.util.generate_value

         # Add timestamp and packet_id to the data
        data =data + (int(time.time()),)
        data =  data + (self.generate_packet_id(),)
        payload_str = json.dumps(data)

        try:
                       
            self.client.publish(self.topic, payload=payload_str)
            print(f'Published: {payload_str}')

            
            sleep(self.delay)

        except mqtt.MQTTException as e:
            print(f'MQTT Exception: {e}')



    def __del__(self):
        self.client.disconnect()    


pub = Publisher()
pub.publish(2)

