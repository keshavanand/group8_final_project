import paho.mqtt.client as mqtt
import json
from time import sleep
import time
from tkinter import Tk, Label, Entry, Button, Text, END
import uuid
import random
from Group8_COMP216_Lab6_Data_Generator import *
import threading



class Publisher:
    def __init__(self, topic='COMP216', delay=1):
        self.util = DataGenerator(data_range=(200, 1100))
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        self.running = False
        self.thread = None


    def generate_packet_id(self):
        packet_id = str(uuid.uuid4())
        return packet_id

    def __publish(self):
        if self.running:
            data = self.util.generate_value

            # Add timestamp and packet_id to the data
            data = data + (int(time.time()),)
            data = data + (self.generate_packet_id(),)
            payload_str = json.dumps(data)

            try:
                self.client.publish(self.topic, payload=payload_str)
                print(f'Published: {payload_str}')
                

            except mqtt.MQTTException as e:
                print(f'MQTT Exception: {e}')

            self.root.after(int(self.delay * 1000), self.__publish)

    def start_publishing(self):
        self.running = True
        self.thread = threading.Thread(target=self.__publish)
        self.thread.start()

    def stop_publishing(self):
         self.running = False
         if self.thread:
            self.thread.join()  # Wait for the thread to finish
         self.client.disconnect()

    def __del__(self):
        if self.client.is_connected():
            self.client.disconnect()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Publisher")

        self.label_topic = Label(root, text="Topic:")
        self.label_topic.grid(row=0, column=0)

        self.entry_topic = Entry(root)
        self.entry_topic.grid(row=0, column=1)

        self.label_delay = Label(root, text="Delay (s):")
        self.label_delay.grid(row=1, column=0)

        self.entry_delay = Entry(root)
        self.entry_delay.grid(row=1, column=1)

        self.start_button = Button(root, text="Start", command=self.start_publisher)
        self.start_button.grid(row=2, column=0, pady=10)

        self.stop_button = Button(root, text="Stop", command=self.stop_publisher)
        self.stop_button.grid(row=2, column=1, pady=10)

        self.output_text = Text(root, height=10, width=50)
        self.output_text.grid(row=3, column=0, columnspan=2)

        self.publisher = None

    def start_publisher(self):
        topic = self.entry_topic.get()
        delay = float(self.entry_delay.get())
        self.publisher = Publisher(topic=topic, delay=delay)
        self.publisher.client.connect('localhost', 1883)
        self.publisher.root = self.root  # Pass 
        self.publisher.start_publishing()

    def stop_publisher(self):
        try:
            if self.publisher:
                self.publisher.stop_publishing()
                del self.publisher  # Disconnect and clean up the publisher instance
        except Exception as e :
            print(e)

    def append_output(self, text):
        self.output_text.insert(END, text + '\n')


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()