import numpy as np



FREQ = 10
MOVE = 64

# RGB memory
K = 10
MEM = [
        [0 for _ in range(K)],
        [0 for _ in range(K)],
        [0 for _ in range(K)],
        ]

def update(t, LED):

    # Update colors
    if t % FREQ == 0:
        # Update colors
        for i in range(3):
            r = np.random.randint(3) - 1
            v = min(255, max(0, MEM[i][-1] + r * MOVE))
            MEM[i] = MEM[i][1:] + [v]

        print(MEM)


    ARR = np.zeros((LED, 3))
    for l in range(LED):
        ti = t % FREQ
        a = (l+ti) // FREQ
        b = (l+ti) % FREQ
           
        for i in range(3):
            #w = np.sin(b / FREQ * np.pi / 2)
            w = np.arctan(b / FREQ * np.pi / 2)
            ARR[l, i ] = MEM[i][a] * (1 - w) + MEM[i][a+1] * w


    return ARR.astype(int)


def create_line(LED):
    return lambda t: update(t, LED)

def create_matrix(LED_x, LED_y):
    return lambda t: update(t, LED_x * LED_y)

def create_border(LED_x, LED_y):
    return lambda t: update(t, (LED_x + LED_y)*2)

