from operator import *
users = [{'key':15615,'val':'helo'},
         {'key':2515,'val':'hey'},
         {'key':2121,'val':'polpc'}
         ]
for x in sorted(users,key = att):
    print(x)