import random
import tkinter as tk
from tkinter import Entry, Button, Canvas, Label, Frame
from tkinter import ttk  # Import ttk for themed buttons

from Group8_COMP216_Lab6_Data_Generator import DataGenerator

class DisplayGauge:
    def __init__(self, root, data_generator):
        self.root = root
        self.root.title('Average Mall Visitors And Time')

        # Frame for the gauge
        self.gauge_frame = Frame(root)
        self.gauge_frame.pack(side=tk.LEFT)

        # Title label for the gauge frame
        gauge_title_label = Label(self.gauge_frame, text='Mall Visitor Analysis \n Choose Time To Check Mall Visitors\n', font=('Arial', 12))
        gauge_title_label.pack()

        self.gauge_canvas = Canvas(self.gauge_frame, width=300, height=300)
        self.gauge_canvas.pack()

        self.label = Label(self.gauge_frame, text='Time: 9 - 23:')
        self.label.pack()

        # Entry field for time input with default value 9
        self.time_entry = Entry(self.gauge_frame)
        self.time_entry.insert(0, '9')
        self.time_entry.pack(side=tk.LEFT)

        # Up arrow button
        # self.up_button = ttk.Button(self.gauge_frame, text='\u25B2', command=lambda: self.update_time(1))
        # self.up_button.pack(side=tk.LEFT)

        # # Down arrow button
        # self.down_button = ttk.Button(self.gauge_frame, text='\u25BC', command=lambda: self.update_time(-1))
        # self.down_button.pack(side=tk.LEFT)

        # Enter button to update the time and enter
        self.update_button = Button(self.gauge_frame, text='Enter', command=self.update_gauge)
        self.update_button.pack()


        self.data_generator = data_generator

        # Initialize the gauge with 0 visitors (grey color)
        self.draw_gauge(0, outline='grey')

        # Creating a dictionary to store visitors count for each unique time
        self.visitors_cache = {}

        # Fixed range of time values from 09 to 23
        self.time_range = [str(i).zfill(2) for i in range(9, 23)]

        # Update the gauge with the default value
        self.update_gauge()

    def update_time(self, increment):
        current_time = self.time_entry.get()
        try:
            current_time = int(current_time)
            new_time = current_time + increment
            if 9 <= new_time <= 23:
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, str(new_time))
                self.update_gauge()  # Update the gauge after changing the time
        except ValueError:
            pass  # Ignore non-integer values in the time entry

    def update_gauge(self):
        time = self.time_entry.get()
        if time:
            # Check if visitors count for the given time is cached
            if time in self.visitors_cache:
                visitors = self.visitors_cache[time]
            else:
                visitors, error_message = self.get_visitors(time)

                if error_message:
                    # Display error message
                    self.label.config(text=error_message)
                else:
                    self.label.config(text='Time (09-23):')
                    self.visitors_cache[time] = visitors  # Cache the visitors count

            self.draw_gauge(visitors, outline='blue')

    def draw_gauge(self, value, outline):
        self.gauge_canvas.delete('all')

        # add labels around the gauge
        label_top = Label(self.gauge_frame, text='0', font=('Arial', 10))
        label_top.place(x=150, y=50, anchor='center')
        
        label_left = Label(self.gauge_frame, text='250', font=('Arial', 10))
        label_left.place(x=20, y=175, anchor='center')

        label_bottom = Label(self.gauge_frame, text='500', font=('Arial', 10))
        label_bottom.place(x=150, y=250, anchor='center')

        label_right = Label(self.gauge_frame, text='1000', font=('Arial', 10))
        label_right.place(x=270, y=175, anchor='center')

        cx, cy, radius = 150, 150, 100
        max_value = 1200
        if value > max_value:
            value = max_value

        angle = min((value / max_value) * 360, 360)  # Adjusting the angle for values greater than 1200

        # Generate a random color for the outline
        outline_color = '#{:02X}{:02X}{:02X}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Create an arc with the random outline color
        self.gauge_canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=90, extent=angle, style=tk.ARC, outline=outline_color, width=20)

        # Add a label
        self.gauge_canvas.create_text(cx, cy, text=f'{value} Visitors', font=('Arial', 12))

    def get_visitors(self, time):
        try:
            time = float(time)
            if 9 <= time <= 23:
                day_index = int(time - 9)
                normalized_value = self.data_generator._DataGenerator__generate_normalized_value(day_index)
                min_val, max_val = self.data_generator.data_range
                value = (max_val - min_val) * normalized_value + min_val
                return int(value), None
            else:
                return 0, 'Invalid time. Please enter a time between 09 and 23.'
        except ValueError:
            return 0, 'Invalid input. Please enter a valid numeric time.'

def main():
    root = tk.Tk()
    mall_data_gen = DataGenerator(data_range=(0, 1000))
    app = DisplayGauge(root, mall_data_gen)
    root.mainloop()

if __name__ == '__main__':
    main()
