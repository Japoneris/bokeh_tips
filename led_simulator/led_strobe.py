"""
Pattern: Rain light

"""
import numpy as np


class Strip:

    def __init__(self, LED, eps=0.005, alpha=0.95):
        # RGB array
        self.N = LED
        self.arr = np.zeros((LED, 3))
        self.eps = eps
        self.alpha = alpha
        return

    def update(self, t=None):
        
        # Move
        mem = self.arr[0]
        for i in range(self.N - 1):
            self.arr[i] = self.arr[i+1] * self.alpha

        # last one
        self.arr[-1] = mem * self.alpha

        # Select LED that become bright
        for i in range(self.N):
            r = np.random.rand()
            if r < self.eps:
                
                
                c = np.random.randint(3)
                self.arr[i, c] = min(255, self.arr[i, c] + 200)
                
                #self.arr[i, :] = [255, 255, 255]
        
        return self.arr.astype(int)



def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

