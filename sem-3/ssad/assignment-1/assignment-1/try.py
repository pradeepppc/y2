class parent:
    lives  = [3]
    def __init__(self):
        pass
    def dec(self):
        self.lives[0] -=1
    def give(self):
        return  self.lives[0]

class person(parent):
    def __init__(self):
        parent.__init__(self)

p1 = person()
p2 = person()

print(p1.give())
print(p2.give())
p1.dec()
p2.dec()
print(p1.give())
print(p2.give())