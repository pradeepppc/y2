import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def ani(z):
    ack = anime()
    xi = ack[0]
    yi = ack[1]
    ax1.clear()
    ax1.plot(xi,yi)



def anime():
    x = input('Enter the number of experiments: \n')
    y = input('Enter the number of steps: \n')
    xs = []
    ys = []
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
    ans = []
    ans.append(xs)
    ans.append(ys)
    return ans

anix = animation.FuncAnimation(fig,ani ,interval=1000)
plt.show()