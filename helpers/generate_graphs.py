import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import argparse
import matplotlib.pyplot as plt

from simulation import Simulation


# colors
FACECOLOR = (230 / 255, 230 / 255, 230 / 255)
CWHITE = (0 / 255, 0 / 255, 0 / 255)
PRIMARYCOLOR = (50 / 255, 168 / 255, 82 / 255)


parser = argparse.ArgumentParser(description="Fire Simulator")
parser.add_argument("-f", "--filename")
args = parser.parse_args()

simulation = Simulation(args.filename, v=False)
data = simulation.read_simulation_data()


steps = []
trees_total = []
trees_alive = []
trees_burning = []
trees_burned = []
bushes = []
chickens = []
water = []
empty = []

for i, step_data in enumerate(data):
    trees_total.append(int(step_data["trees_total"]))
    trees_alive.append(int(step_data["trees_alive"]))
    trees_burning.append(int(step_data["trees_burning"]))
    trees_burned.append(int(step_data["trees_burned"]))
    bushes.append(int(step_data["bushes"]))
    chickens.append(int(step_data["chickens"]))
    water.append(int(step_data["water"]))
    empty.append(int(step_data["empty"]))
    steps.append(i)

plt.xlabel("Steps")
plt.plot(steps, trees_total, label="Árvores totais", color="green")
plt.plot(steps, trees_alive, label="Árvores vivas", color="blue")
plt.plot(steps, trees_burning, label="Árvores queimando", color="orange")
plt.plot(steps, trees_burned, label="Árvores queimadas", color="red")
plt.plot(steps, bushes, label="Arbustos", color="pink")
plt.plot(steps, chickens, label="Galinhas", color="gray")
if sum(water) > 0:
    plt.plot(steps, water, label="Água", color="cyan")
plt.plot(steps, empty, label="Vazio", color="brown")
plt.legend()

plt.savefig(os.path.join("scripts", "simulation", "data", "images", f"{args.filename}_simulation_data.png"), dpi=300)