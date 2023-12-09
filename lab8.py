import tkinter as tk
from tkinter import Entry, Button, Canvas, Label, Frame

from Group8_COMP216_Lab6_Data_Generator import DataGenerator

class BarChartGauge:
    def __init__(self, root, data_generator):
        self.root = root
        self.root.title('Average Mall Visitors And Time')

        # Add a description label at the top
        description_label = Label(root, text='Mall Visitor Analysis - Insert Time To Check Mall Visitors Average', font=('Arial', 12))
        description_label.pack()

        # Frame for the gauge
        self.gauge_frame = Frame(root)
        self.gauge_frame.pack(side=tk.LEFT)

        # Title label for the gauge frame (placed at the top)
        gauge_title_label = Label(self.gauge_frame, text='Horizontal Bar Chart Gauge\n\n\n\n\n\n', font=('Arial', 13))
        gauge_title_label.pack(side=tk.TOP)  # Set the side attribute to TOP


        # Canvas widget for the bar gauge
        self.bar_gauge_canvas = Canvas(self.gauge_frame, width=520, height=50)
        self.bar_gauge_canvas.pack()

        # Create a horizontal bar using a Rectangle
        self.bar_gauge = self.bar_gauge_canvas.create_rectangle(50, 15, 290, 40, fill='grey', outline='blue')

        self.label = Label(self.gauge_frame, text='Time (09-23):')
        self.label.pack()

        self.time_entry = Entry(self.gauge_frame)
        self.time_entry.pack()

        # Enter button to update the time and enter
        self.update_button = Button(self.gauge_frame, text='Enter', command=self.update_gauge)
        self.update_button.pack()

        self.data_generator = data_generator

        # Initialize the gauge with zero visitors (grey color)
        self.draw_gauge(0)

        # Create a dictionary to store visitors count for each unique time
        self.visitors_cache = {}

        # We fixed a range of time values from 09 to 23
        self.time_range = [str(i).zfill(2) for i in range(9, 23)]

        
    def get_visitors(self, time):
        try:
            time = float(time)
            if 9 <= time <= 23:
                day_index = int((time - 9) / 2)
                day_index = min(day_index, 6)
                
                # Get the day name from the time
                day_name = list(self.data_generator.data_generators.keys())[day_index]
                data_gen = self.data_generator.data_generators[day_name]
                
                # Directly access the elements of the tuple returned by generate_value
                times, data_points = data_gen.generate_value
                
                # Assuming the structure of data_points is a list
                if data_points:
                    visitors = data_points[0]  # Assuming the first element represents the number of visitors
                    return int(visitors), None
                else:
                    return 0, 'Invalid data generated.'
            else:
                return 0, 'Invalid time. Please enter a time between 09 and 23.'
        except ValueError:
            return 0, 'Invalid input. Please enter a valid numeric time.'

        
    def update_gauge(self):
        time = self.time_entry.get()
        if time:
            # check if visitors count for the given time is cached
            if time in self.visitors_cache:
                visitors = self.visitors_cache[time]
            else:
                visitors, error_message = self.get_visitors(time)

                if error_message:
                    # display error if it occurs
                    self.label.config(text=error_message)
                else:
                    self.label.config(text='Enter Time (09-23):')
                    self.visitors_cache[time] = visitors  # cache the visitors count

            self.draw_gauge(visitors)

    # draw the bar and change color with number of visitors
    def draw_gauge(self, value):
        # if visitors 500 or less
        if value <= 500:
            fill_color = 'green'
        # if visitors 800 or less
        elif value <= 800:
            fill_color = 'yellow'
        # if visitors higher
        else:
            fill_color = 'red'

        label_positions = [(50, 8, '0'), (170, 8, '600'), (290, 8, '1200')]

        for x, y, text in label_positions:
            self.bar_gauge_canvas.create_text(x, y, text=text, font=('Arial', 8), tags='value_label')

        # update the fill color and width of bar gauge
        bar_width = int(200 * (value / 1000))
        # fill color to the bar according to the number of visitors
        self.bar_gauge_canvas.itemconfig(self.bar_gauge, fill=fill_color)
        self.bar_gauge_canvas.coords(self.bar_gauge, 50, 15, 50 + bar_width, 40)

        # Clear previous text after update
        self.bar_gauge_canvas.delete('value_text')

        # Add a label with the new value of visitors
        self.bar_gauge_canvas.create_text(220, 48, text=f'{value} Visitors ', font=('Arial', 8), tags='value_text')

 
        
class MallVisitorDataGenerator:
    def __init__(self):
        # creating different data for different days and storing it in dict
        self.data_generators = {
            'Monday': DataGenerator(data_range=(100, 500), base_shape='sin', noise_level=50),
            'Tuesday': DataGenerator(data_range=(200, 600), base_shape='sin', noise_level=70),
            'Wednesday': DataGenerator(data_range=(300, 700), base_shape='sin', noise_level=90),
            'Thursday': DataGenerator(data_range=(400, 800), base_shape='sin', noise_level=110),
            'Friday': DataGenerator(data_range=(500, 900), base_shape='sin', noise_level=130),
            'Saturday': DataGenerator(data_range=(600, 1000), base_shape='sin', noise_level=150),
            'Sunday': DataGenerator(data_range=(700, 1100), base_shape='sin', noise_level=170)
        }

    # generating data for each day in dict and ploting it on graph
    def generate_data(self):
        days = list(self.data_generators.keys())
        for day in days:
            data_gen = self.data_generators[day]
            num_data_points = 500
            data_points = [data_gen.generate_value() for _ in range(num_data_points)]


#Show everything under main
def main():
    root = tk.Tk()
    mall_data_gen = MallVisitorDataGenerator()
    app = BarChartGauge(root, mall_data_gen)
    root.mainloop()

if __name__ == '__main__':
    main()
