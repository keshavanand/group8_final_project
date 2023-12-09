import paho.mqtt.client as mqtt
import json
from time import sleep
import time
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, Text, END, messagebox, Scrollbar
import uuid
import random
from Group8_COMP216_Lab6_Data_Generator import *
import threading



class Publisher:
    def __init__(self, app, topic='COMP216', delay=1):
        # Initialize the Publisher instance
        self.util = DataGenerator(data_range=(200, 1100))
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay
        self.running = False
        self.thread = None
        self.app = app

    def generate_packet_id(self):
        # Generate a unique packet ID using UUID
        packet_id = str(uuid.uuid4())
        return packet_id
    
    def append_output(self, text):
        # Append output text to the App's output_text widget
        self.app.append_output(text)

    def __publish(self):
        # Main publishing logic within a separate thread
        if self.running:
            data = self.util.generate_value

            # Add timestamp and packet_id to the data
            current_time = time.time()
            packet_id = self.generate_packet_id()
            data = data + (current_time,)
            data = data + (packet_id,)
            payload_str = json.dumps(data)

            try:
                # Publish the payload to the MQTT broker
                self.client.publish(self.topic, payload=payload_str)
    
                # Convert the floating-point time to a datetime object
                date_time_obj = datetime.fromtimestamp(current_time)
                # Format the datetime object as a string
                formatted_date_time = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")

                # Construct output text for display
                output_text = f'Paylod sent -> Time: {formatted_date_time}, Packet ID: {data[-1]}\n'
                print(output_text)
                self.append_output(output_text)   

            except mqtt.MQTTException as e:
                print(f'MQTT Exception: {e}')

            # Schedule the next publishing after the specified delay
            self.app.output_text.yview(END)  # Auto-scroll to the end
            self.root.after(int(self.delay * 1000), self.__publish)

    def start_publishing(self):
        # Start the publishing thread
        self.running = True
        self.thread = threading.Thread(target=self.__publish)
        self.thread.start()

    def stop_publishing(self):
        # Stop the publishing thread and disconnect from the MQTT broker
         self.running = False
         if self.thread:
            self.thread.join()  # Wait for the thread to finish
         self.client.disconnect()
         self.append_output(f'{self.topic} publisher stopped\n')

    def __del__(self):
        # Disconnect from the MQTT broker when the Publisher instance is deleted
        if self.client.is_connected():
            self.client.disconnect()
            self.append_output(f'{self.topic} publisher disconnected\n')



class App:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("MQTT Publisher")

        # Widgets for entering topic and delay values
        self.label_topic = Label(root, text="Topic:")
        self.label_topic.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        self.entry_topic = Entry(root)
        self.entry_topic.grid(row=0, column=1, pady=(10, 0), padx=(0, 10), sticky="ew")
        
        self.label_delay = Label(root, text="Delay (s):")
        self.label_delay.grid(row=1, column=0, pady=(5, 0), padx=(10, 0), sticky="w")
        self.entry_delay = Entry(root)
        self.entry_delay.insert(0, 1)
        self.entry_delay.grid(row=1, column=1, pady=(5, 0), padx=(0, 10), sticky="ew")

        # Buttons for starting and stopping the publisher
        self.start_button = Button(root, text="Start", command=self.start_publisher, width=15)
        self.start_button.grid(row=2, column=0, pady=10, padx=(10, 0), sticky="w")
        self.stop_button = Button(root, text="Stop", command=self.stop_publisher, width=15)
        self.stop_button.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

        # Text widget for displaying output with scroll bar
        self.output_text = Text(root, height=10, width=50, wrap="word", state="disabled")
        self.output_text.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="ew")

        # Scrollbar for the output_text widget
        self.scrollbar = Scrollbar(root, command=self.output_text.yview)
        self.scrollbar.grid(row=3, column=2, pady=(0, 10), sticky="nse")

        self.output_text["yscrollcommand"] = self.scrollbar.set

        # Publisher instance
        self.publisher = None

    def validate_entry_non_empty(self, entry):
        if not entry.get().strip():  # Check if entry is empty after stripping whitespace
            messagebox.showerror("Error", "Topic Entry cannot be empty.")
            return False
        return True

    def validate_delay(self,delay_str):
        # Validate if the delay input is an integer
        try:
            delay = int(delay_str)
            return delay
        except ValueError:
            messagebox.showerror("Error", "Delay must be an integer.")
            return None
        
    def start_publisher(self):
        # Start the publisher with specified topic and delay values
        topic = self.entry_topic.get()
        delay_str = self.entry_delay.get()

        # Validate topic field if its empty or not
        if not self.validate_entry_non_empty(self.entry_topic):
            return

        # Validate delay input if it is integer or not
        delay = self.validate_delay(delay_str)
        if delay is None:
            return
        
        # Create and start the Publisher instance
        self.publisher = Publisher(self,topic=topic, delay=delay)
        self.publisher.client.connect('localhost', 1883)
        self.append_output(f'Publisher {topic} connected with Broker\n')
        self.publisher.root = self.root  # Pass 
        self.publisher.start_publishing()

    def stop_publisher(self):
        try:
            # Stop and clean up the Publisher instance
            if self.publisher:
                self.publisher.stop_publishing()
                del self.publisher  # Disconnect and clean up the publisher instance
        except Exception as e :
            print(e)

    def append_output(self, text):
        # Append output text to the output_text widget
        self.output_text.config(state="normal")  # Enable text modification
        self.output_text.insert(END, text + '\n')
        self.output_text.config(state="disabled")  # Disable text modification
        self.output_text.yview(END)  # Auto-scroll to the end


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()