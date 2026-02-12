"""
Pattern: Simple snake

1. One led is choosen to be bright.
2. The led is bright
3. Contagion to the next
"""
import numpy as np


class Strip:

    def __init__(self, LED, t_move=1, size=4):
        """
        :param t_move: number of tick to wait before moving the dot
        :param size: length of the snake
        """
        # RGB array
        self.N = LED
        self.arr = np.zeros((LED, 3))
        self.current = 0
        self.t_move = t_move
        self.tick = 0
        self.size = size
        return

    def update(self, t=None):
        
        if self.tick % self.t_move == 0:
            # Snake start
            c0 = self.current
            # Snake end
            c1 = (self.current + self.size + 1) % self.N

            self.arr[c0] = [0, 0, 0]
            self.arr[c1] = [255] + np.random.randint(0, 256,2).tolist()
            self.current = (self.current + 1) % self.N

        
        self.tick += 1
        
        return self.arr.astype(int)


