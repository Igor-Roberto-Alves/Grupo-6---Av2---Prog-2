import csv
import os
import pygame
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt

from pygame.locals import *

CSV_KEYS =  ['trees_total', 'trees_alive', 'trees_burning', 'trees_burned', 'bushes', 'chickens', 'water', 'empty', 'firemen', 'birds']

class Simulation():

    def __init__(self, timestamp: str, v: bool=False) -> None:
        self.name = os.path.join("scripts", "simulation", "data", "data", f"{timestamp}_simulation_data.csv")

        if v:
            print(f"Saving simulation data at {self.name}...")

        if not os.path.exists(self.name):
            with open(self.name, "w", newline="") as csvfile:
                fieldnames = CSV_KEYS
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def write_simulation_data(self, data: dict) -> None:
        with open(self.name, "a", newline="") as csvfile:
            fieldnames = CSV_KEYS
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)

    def read_simulation_data(self) -> list:
        print(f"Reading simulation data at {self.name}...")
        data = []
        with open(self.name, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data