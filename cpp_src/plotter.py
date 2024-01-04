from matplotlib import pyplot as plt
import matplotlib.animation as animation
from sys import stdin

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

colors = ['#ffffff',
          '#ccffcc',
          '#99ff99',
          '#66ff66',
          '#33ff33',
          '#00ff00',
          ]
creature_colors = [
    '#0000ff', '#ff0000'
]
population = []
time = []
dims = [int(_) for _ in stdin.readline().split()]
print(dims)
width = dims[0]
height = dims[1]
mass = []
energy = []
pred = []
prey = []
brain = []
def animate(i):
    title = int(stdin.readline())
    massy = int(stdin.readline())
    energyy = int(stdin.readline())
    predy = int(stdin.readline())
    preyy = int(stdin.readline())
    brainy = int(stdin.readline())
    time.append(title)
    # grass_x = [int(_) for _ in stdin.readline().split()]
    # grass_y = [int(_) for _ in stdin.readline().split()]
    # grass_c = [colors[int(_)] for _ in stdin.readline().split()]
    # print(grass_c)
    x = [int(_) for _ in stdin.readline().split()]
    y = [int(_) for _ in stdin.readline().split()]
    c = [creature_colors[int(_)] for _ in stdin.readline().split()]
    population.append(len(x))
    mass.append(massy / len(x))
    energy.append(energyy / len(x))
    pred.append(predy)
    prey.append(preyy)
    brain.append(brainy / len(x))
    ax1.clear()
    ax1.set(xlim=(0, width), ylim=(0, height))
    ax1.autoscale(False)
    # ax1.scatter(grass_x, grass_y, c=grass_c, marker="s")
    ax1.scatter(x, y, c=c)
    ax1.set_title(f"timestep {title}")
    ax2.clear()
    ax2.set_title(f"Population")
    ax2.plot(time, population, c="green", label="total")
    ax2.plot(time, pred, c="red", label="predators")
    ax2.plot(time, prey, c="blue", label='prey')
    ax2.legend()
    ax3.clear()
    ax3.set_title(f"Mass(orange) and Energy(blue)")
    ax3.plot(time, mass, c="orange", label="mass")
    ax3.plot(time, energy, c="blue", label="energy")
    ax3.legend()
    ax4.clear()
    ax4.set_title(f"Brain size")
    ax4.plot(time, brain)
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()