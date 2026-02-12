"""
Pattern: Rain light

"""
import numpy as np


class StripRef:

    def __init__(self, LED, **kwargs):
        
        # RGB array. Default state with nothing
        self.N = LED
        self.arr = np.zeros((LED, 3))
        
        # Feed arguments
        for key, val in kwargs.items():
            setattr(self, key, val)
        
        return

    def update(self, t=None):
        return np.random.randint(0, 256, (self.N, 3)).astype(int)

    def update_line(self, **kargs):
        return self.update(kargs)

    def update_matrix(self, **kargs):
        return self.update(kargs)


