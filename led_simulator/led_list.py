"""
Pattern: LED light

Given a list of RGB color, switch from one to the other.


"""
import numpy as np


class Strip:

    def __init__(self, LED, colors=[[255, 0, 0], [0, 255, 0], [0, 0, 255]], speed=0.05):
        # RGB array
        self.N = LED
        self.arr = np.zeros((LED, 3))
        self.colors = np.array(colors)
        self.l = len(colors)
        self.speed = speed
        self.tick = 0
        return

    def update(self, t=None):
        

        t = self.tick
        for i in range(self.N):
            r = (t + i) * self.speed
            j = int(r) % self.l
            j1 = (j + 1) % self.l
            
            w = r % 1 # Weight in [0, 1]
            c0 = self.colors[j] # Previous color
            c1 = self.colors[j1] # Next color
            # Update the color
            self.arr[i] = c0 * (1 - w) + c1 * w 
        
        self.tick += 1

        return self.arr.astype(int)



def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

