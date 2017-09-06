import matplotlib.pyplot as plt
import random
import math
import numpy as np

m = int(input('numbxer of particles:\n'))
n = int(input('number of steps: \n'))
f = []
tup = []
tup.append(0)
tup.append(0)
tup.append(0)
for x in range(0,m):
    f.append(tup)
e = np.array(f)
for i in range(0,n):
    for y in range(0,m):
        ranx = random.uniform(0,1)
        rany = random.uniform(0,1)
        ranz = random.uniform(0,1)
        if ranx < 0.5:
            e[y][0] = e[y][0] - 1
        else:
            e[y][0] += 1
        if rany < 0.5:
            e[y][1] -= 1
        else:
            e[y][1] += 1
        if ranz < 0.5:
            e[y][2] -= 1
        else:
            e[y][2] += 1



ans = []
max = 0
for y in range(0,m):
    ll = math.pow(e[y][0],2) + math.pow(e[y][1],2) + math.pow(e[y][2],2)

    ans.append(int(math.sqrt(ll)))
    if int(math.sqrt(ll)) > max:
        max = int(math.sqrt(ll))

final = []
xax = []
for yy in range(0,int(max)):
    final.append(0)
    xax.append(yy)
for y in  range(0,m):
    final[int(ans[y])-1] += 1

plt.plot(xax,final,'ro')
plt.ylabel('s(r)')
plt.xlabel('radius')
plt.show()


