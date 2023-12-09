import random
import matplotlib.pyplot as plt
from datetime import datetime

class DataGenerator:
    # constructor to set default values 
    def __init__(self, data_range=(18, 21), base_shape='sin', noise_level=0.2):
        self.data_range = data_range
        self.base_shape = base_shape
        self.noise_level = noise_level

    # generate normalized random values between 0 to 1
    def __generate_normalized_value(self, time_index):
        # List of peak times:
        low_times = [0,14] # 9 AM and 23 PM
        low_mid_times = [1,6,13]
        mid_times = [2,5,7,12]
        mid_high_times = [4,8,11]
        high_times = [3,9,10] # 12 and 6,7PM
        
        if time_index in low_times:
            return random.uniform(0.1,0.15)
        
        if time_index in low_mid_times:
            return random.uniform(0.15,0.3)
        
        if time_index in mid_times:
            return random.uniform(0.3,0.5)
        
        if time_index in mid_high_times:
            return random.uniform(0.5,0.7)
        
        if time_index in high_times:
            return random.uniform(0.7,0.9)

    # property that generate random values based on the given pattern
    @property
    def generate_value(self):
        times = [str(i).zfill(2) for i in range(9, 24)]  # 09 to 23
        data_points = []
        for i, time in enumerate(times):
            print(time)
            normalized_value = self.__generate_normalized_value(i)
            min_val, max_val = self.data_range
            value = (max_val - min_val) * normalized_value + min_val

            # adding noise to the data
            if self.base_shape == 'sin':
                value += self.noise_level * random.uniform(-1, 1)  # adding noise

            data_points.append(value)

        return times, data_points


# usage
if __name__ == '__main__':
    mall_data_gen = DataGenerator(data_range=(50, 1000))

    days, data_points = mall_data_gen.generate_value

    plt.plot(days, data_points)

    plt.xlabel('Time')
    plt.ylabel('Number of Visitors')
    plt.title('Simulated Mall Visitors Data')
    plt.show()
