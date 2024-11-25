import agents as agent
import random
import images_but as im


class Forest:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = agent.vento()
        self.surge_trees = False

    def incendio(self):
        for _ in range(5):
            l = random.randint(im.tela_x // im.cell_size // 4, self.m - 1)
            k = random.randint(0, self.n - 1)
            if (
                isinstance(self.matriz[k][l], agent.Tree)
                and self.matriz[k][l].condition == "alive"
            ):
                self.matriz[k][l].attempt_to_burn(self.matriz, self.vent)

    def update_forest(self):
        fire = True
        for i in range(0, self.n):
            for j in range(im.tela_x // im.cell_size // 4, self.m):
                if isinstance(self.matriz[i][j], agent.Tree) or isinstance(
                    self.matriz[i][j], agent.Bush
                ):

                    if (
                        self.matriz[i][j].condition == "burning"
                        or self.matriz[i][j].condition == "burned"
                    ):
                        fire = False

                    self.matriz[i][j].update_condition(self)

        if fire:
            self.incendio()  # Caso não tenha fogo, causa um incêndio aleatório

    def get_stats(self):
        stats = {
            "trees_total": 0,
            "trees_alive": 0,
            "trees_burning": 0,
            "trees_burned": 0,
            "bushes": 0,
            "water": 0,
            "empty": 0,
        }

        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.matriz[i][j], agent.Bush):
                    stats["bushes"] += 1
                elif isinstance(self.matriz[i][j], agent.Tree):
                    stats["trees_total"] += 1
                    if self.matriz[i][j].condition == "burning":
                        stats["trees_burning"] += 1
                    elif self.matriz[i][j].condition == "burned":
                        stats["trees_burned"] += 1
                    else:
                        stats["trees_alive"] += 1
                elif isinstance(self.matriz[i][j], agent.Barrier):
                    stats["water"] += 1
                elif self.matriz[i][j] != "black":
                    stats["empty"] += 1

        return stats
