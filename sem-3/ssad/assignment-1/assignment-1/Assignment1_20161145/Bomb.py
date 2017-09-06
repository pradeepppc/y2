import time
class Bomb():

    x_cord = 0
    y_cord = 0

    def __init__(self):
        print('bomb created')

    def create_bomb(self,x,y):
        self.x_cord = x
        self.y_cord = y
        tp = []
        tp.append(x)
        tp.append(y)
        return tp



