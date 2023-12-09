import paho.mqtt.client as mqtt
import json
import tkinter as tk

class Subscriber:
    def __init__(self, topic='COMP216'):
        self.root = tk.Tk()
        self.root.title("MQTT Subscriber")

        self.data_text = tk.Text(self.root, height=10, width=50)
        self.data_text.pack()

        self.client = mqtt.Client()
        self.client.on_message = self.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        print(f'Subscriber listening to: {topic}\n...')
        self.root.after(1000, self.block)
        self.root.mainloop()

    def message_handler(self, client, userdata, message):
        payload_str = message.payload.decode("utf-8")
        self.process_message(payload_str)

    def process_message(self, payload_str):
        data = json.loads(payload_str)
        days, data_points, timeStamp, packet_id = data

        # Display data in text format
        text_data = f'Packet ID: {packet_id}, Time: {timeStamp}\n'
        for time, value in zip(days, data_points):
            text_data += f'Time: {time}, Visitors: {value}\n'

        # Display data in visual format
        visual_data = self.draw_lines(days, data_points)

        # Update the GUI
        self.data_text.delete(1.0, tk.END)
        self.data_text.insert(tk.END, text_data + visual_data)

        self.handle_out_of_range(data_points)
        self.handle_missing_data(data_points)

    @staticmethod
    def draw_lines(times, values):
        max_value = max(values)
        visual_data = ""
        for i in range(max_value, 0, -1):
            line = "|"
            for value in values:
                if value >= i:
                    line += "X"
                else:
                    line += " "
            visual_data += line + "\n"

        # Time axis
        time_axis = "+" + "-" * len(times)
        visual_data += time_axis + "\n"
        visual_data += "".join(times) + "\n"

        return visual_data
    
    @staticmethod
    def handle_out_of_range(data_points):
        min_value = 200
        max_value = 1100
        for value in data_points:
            if value < min_value or value > max_value:
                print(f'Out-of-range value detected: {value}')

    @staticmethod
    def handle_missing_data(data_points):
        expected_length = 15  
        if len(data_points) < expected_length:
            print('Missing data detected')

    def block(self):
        self.client.loop()
        self.root.after(1000, self.block)

if __name__ == "__main__":
    sub = Subscriber()
