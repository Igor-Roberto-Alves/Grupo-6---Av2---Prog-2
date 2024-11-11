import os
import random
import pygame
import time
import matplotlib.pyplot as plt

# Inicialização do Pygame
pygame.init()

TREE_ALIVE_IMG = pygame.image.load(os.path.join('images', 'Tree_Small.png'))
ALIVE_TO_BURNING_IMGs = [pygame.image.load(os.path.join('images\\alive_to_burning', f'alive_to_burning_{k}.png')) for k in range(3)]
TREE_BURNING_IMG = pygame.image.load(os.path.join('images', 'Fire_Small.png'))
BURNING_TO_BURNED_IMGs = [pygame.image.load(os.path.join('images\\burning_to_burned', f'burning_to_burned_{k}.png')) for k in range(3)]
WATER_IMG = pygame.image.load(os.path.join('images', "pixil-frame-0 (2).png"))
START_IMG = pygame.image.load(os.path.join('images', "shadedDark42.png"))
TREE_BURNED_IMG = pygame.image.load(os.path.join('images', "pixil-frame-0 (4).png"))

cell_size = 25
TREE_ALIVE_IMG = pygame.transform.scale(TREE_ALIVE_IMG, (cell_size, cell_size))
for i, imagem in enumerate(ALIVE_TO_BURNING_IMGs):
    ALIVE_TO_BURNING_IMGs[i] = pygame.transform.scale(imagem, (cell_size, cell_size))
TREE_BURNING_IMG = pygame.transform.scale(TREE_BURNING_IMG, (cell_size, cell_size))
for i, imagem in enumerate(BURNING_TO_BURNED_IMGs):
    BURNING_TO_BURNED_IMGs[i] = pygame.transform.scale(imagem, (cell_size, cell_size))
WATER_IMG = pygame.transform.scale(WATER_IMG, (cell_size, cell_size))
TREE_BURNED_IMG = pygame.transform.scale(TREE_BURNED_IMG, (cell_size, cell_size))


class Tree:
    def __init__(self, coord):
        self.condition = "alive"
        self.density = random.randint(50, 80)
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0
        self.step = 0

    def neighbors(self, matriz):
        lista = []
        directions = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= nx < len(matriz)
                and 0 <= ny < len(matriz[0])
                and isinstance(matriz[nx][ny], Tree)
            ):
                lista.append(matriz[nx][ny])
        return lista

    def attempt_to_burn(self, matriz, vent):

        if self.condition == "alive":
            self.next_condition = "burning"
            for neighbor in self.neighbors(matriz):
                if (
                    neighbor.condition == "alive"
                    and neighbor.next_condition != "burning"
                ):
                    probability = 100 - neighbor.density
                    if vent.directions:
                        if neighbor in vent.neighbors_vento(self, matriz):
                            probability = min(80, probability + 30)
                        else:
                            probability = max(40, probability - 20)
                    if (
                        random.random() < probability / 100
                    ):  # queima o vizinho com probabilidade 1 - densidade da árvore
                        neighbor.next_condition = "tick"

    def burn_continuos(self, matriz, vent):
        for neighbor in self.neighbors(matriz):
            if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                probability = min(100 - neighbor.density - 40, 10)
                if vent.directions:
                    if neighbor in vent.neighbors_vento(self, matriz):
                        probability = min(60, probability + 10)
                    else:
                        probability = max(10, probability - 20)
                if (
                    random.random() < probability / 100
                ):  # queima o vizinho com probabilidade 1 - densidade da árvore
                    neighbor.next_condition = "tick"

    def update_condition(self, forest):
        matriz = forest.matriz
        vent = forest.vent
        if self.next_condition == "burned":
            self.next_condition = "step"
            self.condition = "burned"
            self.burn_continuos(matriz, vent)

        elif self.next_condition == "step":
            self.step += 1
            self.burn_continuos(matriz, vent)
            if self.step == 3:
                self.next_condition = "final"

        elif self.next_condition == "final":
            matriz[self.x][self.y] = "v"

        if self.next_condition == "burning":  # Se o próximo estágio é queimando
            self.attempt_to_burn(matriz, vent)  # queima os vizinhos
            self.count += 1
            self.condition = self.next_condition
            if self.count == 4:
                self.next_condition = "burned"

        if (
            self.next_condition == "tick"
        ):  # tick pode ser usado para melhorar a transição entre alive e burning
            self.next_condition = "burning"

    def __repr__(self):  # para visualizar a matriz
        if self.condition == "alive":
            return "1"
        if self.condition == "burning":
            return "b"
        if self.condition == "burned":
            return "0"


class Barrier:  # representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return "a"


class Houses:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[0]

    def __repr__(self):
        return "h"


class vento:
    def __init__(self, direction=None):
        lista_directions = ["N", "S", "L", "O", "NO", "NE", "SE", "SO"]
        self.directions = []
        if direction == 1:
            direction = random.choice(lista_directions)
        if direction == "L":
            self.directions = [(0, 1), (1, 1), (-1, 1)]
        elif direction == "O":
            self.directions = [(0, -1), (1, -1), (-1, -1)]
        elif direction == "S":
            self.directions = [(1, 0), (1, 1), (1, -1)]
        elif direction == "N":
            self.directions = [(-1, 0), (-1, 1), (-1, -1)]
        elif direction == "SE":
            self.directions = [(0, 1), (1, 0), (1, 1)]
        elif direction == "NE":
            self.directions = [(0, 1), (-1, 0), (-1, 1)]
        elif direction == "SO":
            self.directions = [(0, -1), (1, 0), (1, -1)]
        elif direction == "NO":
            self.directions = [(0, -1), (-1, 0), (-1, -1)]

    def neighbors_vento(self, tree, matriz):
        lista = []
        if self.directions:
            for dx, dy in self.directions:
                nx, ny = tree.x + dx, tree.y + dy
                if (
                    0 <= nx < len(matriz)
                    and 0 <= ny < len(matriz[0])
                    and isinstance(matriz[nx][ny], Tree)
                ):
                    lista.append(matriz[nx][ny])

        return lista


class Forest:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = vento(1)

    def incendio(self):
        while True:
            k = random.randint(0, self.n - 1)
            l = random.randint(0, self.m - 1)
            if (
                isinstance(self.matriz[k][l], Tree)
                and self.matriz[k][l].condition == "alive"
            ):
                self.matriz[k][l].attempt_to_burn(self.matriz, self.vent)
                break

    def update_forest(self):
        for row in self.matriz:
            for cell in row:
                if isinstance(cell, Tree):
                    cell.update_condition(self)

    def extinguish_tree_at(self, x, y):
        col, row = x // cell_size, y // cell_size
        if 0 <= row < self.n and 0 <= col < self.m:
            cell = self.matriz[row][col]
            if isinstance(cell, Tree):
                cell.extinguish_fire()

    def surge_trees(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.matriz[i][j] == "v":
                    a = random.randint(1, 5)
                    if a == 1:
                        self.matriz[i][j] = Tree((i, j))

    def tree_f_pos(self, coord):
        self.matriz[coord[0]][coord[1]] == Tree((coord[0], coord[1]))


def draw_forest(screen, forest, state):
    def transition_alive_to_burning(i,j,state):
        if state < 3:
            screen.blit(ALIVE_TO_BURNING_IMGs[state], (j * cell_size, i * cell_size))
        else:
            screen.blit(TREE_BURNING_IMG, (j * cell_size, i * cell_size))
    def transition_burning_to_burned(i,j,state):
        if state < 3:
            screen.blit(BURNING_TO_BURNED_IMGs[state], (j * cell_size, i * cell_size))
        else:
            screen.blit(TREE_BURNED_IMG, (j * cell_size, i * cell_size))

    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, Tree):
                if cell.condition == "alive":
                    screen.blit(TREE_ALIVE_IMG, (j * cell_size, i * cell_size))
                elif cell.condition == "burning":
                    transition_alive_to_burning(i,j,state) # Animação de transição, viva pra queimando.
                elif cell.condition == "burned":
                    transition_burning_to_burned(i,j,state) # Animação de transição, queimando para queimada.
            elif isinstance(cell, Barrier):
                # pygame.draw.rect(screen, (173, 216, 230), (j * cell_size, i * cell_size, cell_size, cell_size))
                screen.blit(WATER_IMG, (j * cell_size, i * cell_size))
            if cell == "v":
                pygame.draw.rect(
                    screen,
                    (85, 107, 47),
                    (j * cell_size, i * cell_size, cell_size, cell_size),
                )


def main():
    screen_width, screen_height = 1500, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((85, 107, 47))
    pygame.display.set_caption("Forest Fire Simulation")

    matriz = [[Tree((i, j)) for j in range(60)] for i in range(28)]

    forest = Forest(matriz)
    forest.vent = (
        vento()
    )  # A floresta agora estará sobre a ação de um vento com direção aleatória
    print(forest.vent.directions)
    alive_burning_burned = []
    running = True
    button_width, button_height = START_IMG.get_width(), START_IMG.get_height()
    button_x, button_y = 30 * cell_size, 15 * cell_size

    def is_button_clicked(pos):
        return (
            button_x <= pos[0] <= button_x + button_width
            and button_y <= pos[1] <= button_y + button_height
        )

    # Flag que controla a exibição do botão
    button_visible = True
    start = False  # Controle para verificar se o incêndio deve iniciar
    state = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_button_clicked(event.pos) and button_visible:
                    print("Botão clicado!")
                    button_visible = False  # Esconde o botão após o clique
                    start = True  # Inicia o incêndio após o clique

        screen.fill((85, 107, 47))
        draw_forest(screen, forest, state)

        # Desenhar o botão apenas se ele estiver visível
        if button_visible:
            screen.blit(START_IMG, (button_x, button_y))

        pygame.display.flip()  # Atualiza a tela

        if start:
            forest.incendio()  # Inicia o incêndio
            start = False

        burned = 0
        burning = 0
        alive = 0
        incendio = True
        for row in matriz:
            for cell in row:
                if cell == "v":
                    burned += 1
                if isinstance(cell, Tree):
                    if cell.condition == "alive":
                        alive += 1
                    if cell.condition == "burning":
                        burning += 1
                    if cell.next_condition == "burning":
                        incendio = False
        if incendio:
            pass
            # forest.incendio() #caso o incêndio acabe inicia um novo

        alive_burning_burned.append((alive, burning, burned))

        forest.update_forest()
        
        if state == 3:
            state = 0
        else:
            state += 1
        time.sleep(0.1)

    pygame.quit()

    def graph():
        first_values = [item[0] for item in alive_burning_burned]
        second_values = [item[1] for item in alive_burning_burned]
        third_values = [item[2] for item in alive_burning_burned]
        x = list(range(len(alive_burning_burned)))
        plt.plot(x, first_values, label="Árvores vivas")
        plt.plot(x, second_values, label="Árvores queimando")
        plt.plot(x, third_values, label="Árvores queimadas")

        plt.title("Gráfico de três curvas com valores dos trios")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.legend()

        plt.show()


if __name__ == "__main__":
    main()
