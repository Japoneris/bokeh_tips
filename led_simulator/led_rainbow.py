"""
Pattern: Rain light

"""
import numpy as np
from led_prototype import StripRef


class Strip(StripRef):

    def __init__(self, LED, speed=0.05):
        self.LED = LED
        self.arr = np.zeros((LED, 3))
        self.tick = 0
        self.speed = speed
        return 

    def update(self, **kwargs):
        
        T = (np.arange(self.LED) + self.tick) * self.speed

        # Set color
        for idx, v in enumerate([3, 5, 7]):
            self.arr[:, idx] = 128 * (1 + np.cos(T * v))
        

        self.tick += 1

        return self.arr.astype(int).clip(0, 255)

    def update_line(self, **kargs):
        return self.update(kargs)

    def update_matrix(self, **kargs):
        return self.update(kargs)


