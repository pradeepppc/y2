from Person import *
from Bomb import *
class Enemy(Person):
    life = 1
    name = 'enemy'

    def __init__(self):
        Person.__init__(self)

    def Kill_by_bomb(self):
        self.life = 0
    def get_life(self):
        return self.life








