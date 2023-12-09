import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt


class Subscriber:
    def __init__(self, topic='COMP216'):
        self.client = mqtt.Client()
        self.client.on_message = Subscriber.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        print(f'Subscriber listening to: {topic}\n...')

    @staticmethod
    def message_handler(client, userdata, message):
        print(f'\nTopic: {message.topic}')
        Subscriber.process_message(message.payload.decode("utf-8"))

    @staticmethod
    def process_message(payload_str):
       
        data = json.loads(payload_str)

        
        days, data_points, timeStamp,packet_id = data
        plt.plot(days, data_points)

        plt.xlabel('Time')
        plt.ylabel('Number of Visitors')
        plt.title('Simulated Mall Visitors Data')
        plt.show()

        print(f'"Packet ID: "{packet_id},"Time: "{timeStamp}')


    def block(self):
        self.client.loop_forever()

sub = Subscriber()
sub.block()