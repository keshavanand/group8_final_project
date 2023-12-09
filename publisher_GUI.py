import paho.mqtt.client as mqtt
import json
from time import sleep
import time
from tkinter import Tk, Label, Entry, Button, Text, END, messagebox, Scrollbar
import uuid
import random
from Group8_COMP216_Lab6_Data_Generator import *
import threading



class Publisher:
    def __init__(self, app, topic='COMP216', delay=1):
        self.util = DataGenerator(data_range=(200, 1100))
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        self.running = False
        self.thread = None
        self.app = app

    def generate_packet_id(self):
        packet_id = str(uuid.uuid4())
        return packet_id
    
    def append_output(self, text):
        self.app.append_output(text)

    def __publish(self):
        if self.running:
            data = self.util.generate_value

            # Add timestamp and packet_id to the data
            data = data + (int(time.time()),)
            data = data + (self.generate_packet_id(),)
            payload_str = json.dumps(data)

            try:
                self.client.publish(self.topic, payload=payload_str)
    
                output_text = f'Time: {data[-2]}, Packet ID: {data[-1]}'
                print(output_text)
                self.append_output(output_text)   

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
        self.label_topic.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")

        self.entry_topic = Entry(root)
        self.entry_topic.grid(row=0, column=1, pady=(10, 0), padx=(0, 10), sticky="ew")

        self.label_delay = Label(root, text="Delay (s):")
        self.label_delay.grid(row=1, column=0, pady=(5, 0), padx=(10, 0), sticky="w")

        self.entry_delay = Entry(root)
        self.entry_delay.insert(0, 1)
        self.entry_delay.grid(row=1, column=1, pady=(5, 0), padx=(0, 10), sticky="ew")

        self.start_button = Button(root, text="Start", command=self.start_publisher, width=15)
        self.start_button.grid(row=2, column=0, pady=10, padx=(10, 0), sticky="w")

        self.stop_button = Button(root, text="Stop", command=self.stop_publisher, width=15)
        self.stop_button.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

        self.output_text = Text(root, height=10, width=50, wrap="word", state="disabled")
        self.output_text.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="ew")

        self.scrollbar = Scrollbar(root, command=self.output_text.yview)
        self.scrollbar.grid(row=3, column=2, pady=(0, 10), sticky="nse")

        self.output_text["yscrollcommand"] = self.scrollbar.set

        self.publisher = None

    def validate_entry_non_empty(self, entry):
        if not entry.get().strip():  # Check if entry is empty after stripping whitespace
            messagebox.showerror("Error", "Topic Entry cannot be empty.")
            return False
        return True

    def validate_delay(self,delay_str):
        try:
            delay = int(delay_str)
            return delay
        except ValueError:
            messagebox.showerror("Error", "Delay must be an integer.")
            return None
        
    def start_publisher(self):
        topic = self.entry_topic.get()
        delay_str = self.entry_delay.get()

        # Validate topic field if its empty or not
        if not self.validate_entry_non_empty(self.entry_topic):
            return

        # Validate delay input if it is integer or not
        delay = self.validate_delay(delay_str)
        if delay is None:
            return
        
        self.publisher = Publisher(self,topic=topic, delay=delay)
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
        self.output_text.config(state="normal")  # Enable text modification
        self.output_text.insert(END, text + '\n')
        self.output_text.config(state="disabled")  # Disable text modification
        self.output_text.yview(END)  # Auto-scroll to the end


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()