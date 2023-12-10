import random
import tkinter as tk
from tkinter import Entry, Canvas, Label, Frame
from tkinter import ttk  # Import ttk for themed buttons

from Group8_COMP216_Lab6_Data_Generator import DataGenerator

class DisplayBarChart:
    def __init__(self, root, data_generator):
        self.root = root
        self.root.title('Average Mall Visitors And Time')

        # Frame for the bar chart
        self.bar_chart_frame = Frame(root)
        self.bar_chart_frame.pack(side=tk.LEFT)

        # Title label for the bar chart frame
        bar_chart_title_label = Label(self.bar_chart_frame, text='Mall Visitor Analysis\nChoose Time To Check Mall Visitors\n', font=('Arial', 12))
        bar_chart_title_label.pack()

        self.bar_chart_canvas = Canvas(self.bar_chart_frame, width=340, height=300)
        self.bar_chart_canvas.pack()

        self.label = Label(self.bar_chart_frame, text='Time: 9 - 23:')
        self.label.pack()

        # Entry field for time input with default value 9
        self.time_entry = Entry(self.bar_chart_frame)
        self.time_entry.insert(0, '9')
        self.time_entry.pack(side=tk.LEFT, padx=20)

        # Up arrow button
        self.up_button = ttk.Button(self.bar_chart_frame, text='\u25B2', command=lambda: self.update_time(1))
        self.up_button.pack(side=tk.LEFT, padx=5)

        # Down arrow button
        self.down_button = ttk.Button(self.bar_chart_frame, text='\u25BC', command=lambda: self.update_time(-1))
        self.down_button.pack(side=tk.LEFT)

        self.data_generator = data_generator

        # Initialize the bar chart with 0 visitors (grey color)
        self.draw_chart(0, outline='grey')

        # Creating a dictionary to store visitors count for each unique time
        self.visitors_cache = {}

        # Fixed range of time values from 09 to 23
        self.time_range = [str(i).zfill(2) for i in range(9, 23)]

        # Update the bar chart with the default value
        self.update_chart()

    def update_time(self, increment):
        current_time = self.time_entry.get()
        try:
            current_time = int(current_time)
            new_time = current_time + increment
            if 9 <= new_time <= 23:
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, str(new_time))
                self.update_chart()  # Update the bar chart after changing the time
        except ValueError:
            pass  # Ignore non-integer values in the time entry

    def update_chart(self):
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
                    self.label.config(text='Time: 9 - 23')
                    self.visitors_cache[time] = visitors  # Cache the visitors count

            self.draw_chart(visitors, outline='blue')

    def draw_chart(self, value, outline):
        self.bar_chart_canvas.delete('all')

        # add labels around the chart
        base_x = 20
        max_x = 300
        label_left = Label(self.bar_chart_frame, text='0', font=('Arial', 10))
        label_left.place(x=base_x+0, y=175, anchor='center')

        label_bottom = Label(self.bar_chart_frame, text='250', font=('Arial', 10))
        label_bottom.place(x=(base_x+max_x)*0.25, y=175, anchor='center')

        label_bottom = Label(self.bar_chart_frame, text='500', font=('Arial', 10))
        label_bottom.place(x=(base_x+max_x)*0.5, y=175, anchor='center')
        
        label_bottom = Label(self.bar_chart_frame, text='750', font=('Arial', 10))
        label_bottom.place(x=(base_x+max_x)*0.75, y=175, anchor='center')

        label_right = Label(self.bar_chart_frame, text='1000', font=('Arial', 10))
        label_right.place(x=base_x+max_x, y=175, anchor='center')

        max_value = 1000
        if value > max_value:
            value = max_value

        # Generate a random color for the outline
        outline_color = '#{:02X}{:02X}{:02X}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Calculate the width of the bar chart
        bar_width = int(max_x * (value / max_value))

        # Create a horizontal bar using a Rectangle with the random outline color
        self.bar_chart_canvas.create_rectangle(base_x+0, 130, base_x + bar_width, 180, fill=outline_color, outline=outline, width=2)

        # Add a label
        self.bar_chart_canvas.create_text(150, 200, text=f'{value} Visitors', font=('Arial', 12))

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
    app = DisplayBarChart(root, mall_data_gen)
    root.mainloop()

if __name__ == '__main__':
    main()
