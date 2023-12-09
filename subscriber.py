import paho.mqtt.client as mqtt
import json



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

        days, data_points, timeStamp, packet_id = data

        # Display data in text format
        print(f'Packet ID: {packet_id}, Time: {timeStamp}')
        for time, value in zip(days, data_points):
            print(f'Time: {time}, Visitors: {value}')

        # Display data in visual format
        Subscriber.draw_lines(days, data_points)

    @staticmethod
    def draw_lines(times, values):
        max_value = max(values)
        for i in range(max_value, 0, -1):
            line = "|"
            for value in values:
                if value >= i:
                    line += "X"
                else:
                    line += " "
            print(line)

        # Print time axis
        time_axis = "+" + "-" * len(times)
        print(time_axis)
        print("".join(times))

    def block(self):
        self.client.loop_forever()

if __name__ == "__main__":
    sub = Subscriber()
    sub.block()