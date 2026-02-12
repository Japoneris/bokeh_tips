"""
Pattern: Rain light

"""
import numpy as np


class Strip:

    def __init__(self, LED, eps=0.01, alpha=0.80):
        # RGB array
        self.N = LED
        self.arr = np.zeros((LED, 3))
        self.eps = eps
        self.alpha = alpha
        return

    def update(self, t=None):
        
        self.arr = self.alpha * self.arr
        A = np.concatenate([self.arr[1:], [self.arr[0]]])
        B = np.concatenate([[self.arr[-1]], self.arr[:-1]])

        ai = (1 - self.alpha)/2
        
        self.arr = (self.arr + (A + B) * ai).clip(0, 255)

        # Select LED that become bright
        for i in range(self.N):
            r = np.random.rand()
            if r < self.eps:
                
                self.arr[i] = (self.arr[i] + np.array([200, 150, 200])).clip(0, 255)
                
                #self.arr[i, :] = [255, 255, 255]
        
        return self.arr.astype(int)



def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

