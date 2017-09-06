import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
import math
import random

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def ani():
    ack = anime()
    xi = ack[0]
    yi = ack[1]
    zi = ack[2]
    fig = plt.figure()
    ax = fig.add_subplot(111, label='1')
    ax2 = fig.add_subplot(111 , label ='2',frame_on = False)
    ax.plot(xi,yi,color = 'C0')
    ax.set_xlabel("x label 1", color="C0")
    ax.set_ylabel("y label 1", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    ax2.scatter(xi,zi,color= 'C1')
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.set_xlabel('x label 2', color="C1")
    ax2.set_ylabel('y label 2', color="C1")
    ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='x', colors="C1")
    ax2.tick_params(axis='y', colors="C1")

    plt.show()

def anime():
    x = input('Enter the number of experiments: \n')
    y = input('Enter the number of steps: \n')
    xs = []
    ys = []
    acts = []
    for k in range(0,int(y)):
        ans = 0
        xs.append(k)
        for i in range(0,int(x)):
            dis1 = 0
            dis2 = 0
            for j in range(0,int(k)):
                r1 = random.uniform(0,1)
                r2 = random.uniform(0,1)
                if r1 < 0.5:
                    dis1 -= 1
                else:
                    dis1 += 1

                if r2 < 0.5:
                    dis2 -= 1
                else:
                    dis2 += 1
            if dis1 == dis2:
                ans += 1

        prob = ans/float(x)
        ys.append(prob)
        anns = factorial(k)
        ans1 = (factorial(2*k)/(anns*anns))*(1/math.pow(2,2*k))
    ans = []
    acts.append(ans1)
    ans.append(xs)
    ans.append(ys)
    ans.append(acts)
    return ans

ani()