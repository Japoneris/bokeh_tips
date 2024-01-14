import numpy as np


# RGB parameters
BASE = [100, 150, 200]
AMPL = [60, 40, 30]
SPEED = [50, 10, 43]
STRIDE = [20, 5, 7]

def update(t, LED):


    lll = np.arange(LED)

    RGB = []
    for i in range(3): # RGB iteration:
        tmp = BASE[i] + AMPL[i] * np.sin((lll * STRIDE[i] + t*SPEED[i])/180)
        RGB.append(tmp.astype(int))

    return np.array(RGB).T

def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

