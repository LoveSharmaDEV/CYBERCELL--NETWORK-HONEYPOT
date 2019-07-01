import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('graph1.txt' , 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    x = 0
    for line in lines:
        if len(line) >1:
            y = line
            x = x + 1
            xs.append(x)
            ys.append(y)
    ax1.clear()    
    ax1.plot(xs , ys)

ani = animation.FuncAnimation(fig, animate , interval = 100)
plt.show()

