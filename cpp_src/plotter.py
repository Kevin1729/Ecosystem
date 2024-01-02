from matplotlib import pyplot as plt
import matplotlib.animation as animation
from sys import stdin

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    x = [int(_) for _ in stdin.readline().split()]
    y = [int(_) for _ in stdin.readline().split()]
    ax1.clear()
    ax1.set(xlim=(0, 100), ylim=(0, 100))
    ax1.autoscale(False)
    ax1.scatter(x, y)
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()