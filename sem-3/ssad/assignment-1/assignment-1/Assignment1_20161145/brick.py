class Brick:
    isalive = True
    xcord = 0
    ycord = 0
    def __init__(self):
        pass

    def destroy(self):
        self.isalive = False

    def get_life(self):
        return self.isalive

    def set_cord(self, x, y):
        self.xcord = x
        self.ycord = y

    def ret_cord(self):
        tup = []
        tup.append(self.xcord)
        tup.append(self.ycord)
        return tup

