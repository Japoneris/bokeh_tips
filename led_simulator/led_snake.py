"""
Pattern: Simple snake

1. One led is choosen to be bright.
2. The led is bright
3. Contagion to the next
"""
import numpy as np


class Strip:

    def __init__(self, LED, t_move=5):
        # RGB array
        self.N = LED
        self.arr = np.zeros((LED, 3))
        self.current = 0
        self.t_move = t_move
        self.tick = 0
        return

    def update(self, t=None):
        
        if self.tick % self.t_move == 0:
            self.arr[self.current] = [0, 0, 0] # Reset LED color to black
            self.current = (self.current + 1) % self.N # Move from 1
            self.arr[self.current] = [255, 255, 255]
        
        self.tick += 1
        
        return self.arr.astype(int)



def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

