import numpy as np
class Person():
    x_coord = 0
    y_coord = 0
    def __init__(self):
        pass


    def change_position(self, x, y):
        self.x_coord += x
        self.y_coord += y

    def set_position(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def get_position(self):
        tup = []
        tup.append(self.x_coord)
        tup.append(self.y_coord)
        return tup







