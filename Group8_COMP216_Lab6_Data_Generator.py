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
        
          # just simple pattern bases on even and odd
        if time_index % 2 == 0:  # Even indexes
            if time_index == 0:  # if its 9am it will be lowest
                return random.uniform(0.1,0.2)
            return random.uniform(0.4, 0.6) # otherwise random up down  
        else:  # Odd days
            if time_index == 3: #if its lunch time it will be at peak
                return random.uniform(0.7,0.9)
            if time_index == 13:
                return random.uniform(0.6,0.8) # at movie time it will be higher than normal
            return random.uniform(0.2, 0.4)


    # property that generate random values based on the given pattern
    @property
    def generate_value(self):
        times = [str(i).zfill(2) for i in range(9, 24)]  # 09 to 23
        data_points = []
        for i, time in enumerate(times):
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
    mall_data_gen = DataGenerator(data_range=(200, 1100))

    days, data_points = mall_data_gen.generate_value

    plt.plot(days, data_points)

    plt.xlabel('Time')
    plt.ylabel('Number of Visitors')
    plt.title('Simulated Mall Visitors Data')
    plt.show()
