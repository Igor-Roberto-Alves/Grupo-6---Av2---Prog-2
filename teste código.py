import pygame
import time
import agents as agent 
from forest import Forest 
import images_but as im

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import matplotlib.pyplot as plt

pygame.init()
clock = pygame.time.Clock()

def draw_forest(screen, forest):
    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, agent.Tree):
                if cell.condition == "alive":
                    screen.blit(im.TREE_ALIVE_IMG, (j * im.cell_size, i * im.cell_size))
                elif cell.condition == "burning":
                    screen.blit(im.TREE_BURNING_IMG, (j * im.cell_size, i * im.cell_size))
                elif cell.condition == "burned":
                    screen.blit(im.TREE_BURNED_IMG, (j * im.cell_size, i * im.cell_size))
            elif isinstance(cell, agent.Barrier):
                screen.blit(im.WATER_IMG, (j * im.cell_size, i * im.cell_size))
            elif cell == "v":
                pygame.draw.rect(
                    screen,
                    (95, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )
            elif cell == "black":
                pygame.draw.rect(
                    screen,
                    (105, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )

def draw_bombeiros(screen, lista_bombeiros):
    for bombeiro in lista_bombeiros:
        if bombeiro.status == "alive":
            screen.blit(
                im.FIREMAN_IMG, (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size)
            )
        elif bombeiro.status == "burning":
            screen.blit(
                im.FIREMAN_BURNING2_IMG,
                (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
            )
        elif bombeiro.status == "burning2":
            screen.blit(
                im.FIREMAN_BURNING1_IMG,
                (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
            )

def init_screen():
    screen = pygame.display.set_mode((im.tela_x, im.tela_y))
    matriz = [
        [agent.Tree((i, j)) for j in range(im.tela_x // im.cell_size)]
        for i in range(im.tela_y // im.cell_size)
    ]

    for i in range((im.tela_x // im.cell_size) // 4):
        for j in range(im.tela_y // im.cell_size):
            matriz[j][i] = "black"

    return matriz, screen

# Adiciona a função count_trees na classe Forest
def count_trees(self):
    """
    Conta o número de árvores vivas e queimadas na matriz.
    """
    alive = sum(1 for row in self.matriz for cell in row if isinstance(cell, agent.Tree) and cell.condition == "alive")
    burned = sum(1 for row in self.matriz for cell in row if isinstance(cell, agent.Tree) and cell.condition == "burned")
    return alive, burned

# Adiciona a função à classe Forest dinamicamente (se necessário)
Forest.count_trees = count_trees

def main():
    matriz, screen = init_screen()
    forest = Forest(matriz)  # Inicializando a Floresta
    forest.vent = agent.vento()

    running = True
    start = False
    start2 = False
    loading = False
    bombeiros = [agent.bombeiro(matriz) for _ in range(10)]
    bombeiros_andar = False
    forest.surge_trees = True

    steps_by_second = 30
    TIMERSTEPEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMERSTEPEVENT, 1000 // steps_by_second)

    label = TextBox(screen, 15, 10, 270, 40, fontSize=23)
    label.setText(f"Passos por segundo: {steps_by_second}")
    label.disable()

    slider = Slider(screen, 20, 60, 250, 12, min=1, max=100, step=1, initial=steps_by_second)

    alive_trees = []
    burned_trees = []
    time_steps = []

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if im.start_but.is_button_clicked(event.pos) and im.start_but.visible:
                    if start2:
                        loading = True

                    print("Botão clicado!")
                    im.start_but.visible = False
                    start = True
                    im.pause_but.visible = True
                    bombeiros_andar = True
                    loading = True

                if im.up_but.is_button_clicked(event.pos):
                    print("up clicado")
                    forest.vent = agent.vento("N")

                if im.down_but.is_button_clicked(event.pos):
                    print("down clicado")
                    forest.vent = agent.vento("S")

                if im.right_but.is_button_clicked(event.pos):
                    print("right clicado")
                    forest.vent = agent.vento("L")

                if im.left_but.is_button_clicked(event.pos):
                    print("left clicado")
                    forest.vent = agent.vento("O")

                if im.x_but.is_button_clicked(event.pos):
                    print("x clicado")
                    forest.vent = agent.vento()

                if im.pause_but.is_button_clicked(event.pos):
                    print("pause clicado")
                    im.start_but.visible = True
                    im.pause_but.visible = False
                    start2 = True
                    loading = False
            elif event.type == TIMERSTEPEVENT:
                if start:
                    forest.incendio()
                    start = False

                if loading:
                    a = forest.update_forest()  # Certifique-se de que esse método existe na classe Forest
                    if a:
                        forest.incendio()
                    forest.update_forest()

                    if bombeiros_andar:
                        bombeiros_vivos = [bomb for bomb in bombeiros if bomb.status != "dead"]  # Defina bombeiros_vivos aqui
                        for bombeirx in bombeiros_vivos:
                            bombeirx.andar()
                            bombeirx.atualizar_bombeiro()

                    # Atualiza dados para o gráfico
                    alive, burned = forest.count_trees()
                    alive_trees.append(alive)
                    burned_trees.append(burned)
                    time_steps.append(len(time_steps))

        if slider.getValue() != steps_by_second:
            steps_by_second = slider.getValue()
            pygame.time.set_timer(TIMERSTEPEVENT, 1000 // steps_by_second)

        screen.fill((85, 107, 47))
        draw_forest(screen, forest)
        bombeiros_vivos = [bomb for bomb in bombeiros if bomb.status != "dead"]  # Defina bombeiros_vivos aqui
        draw_bombeiros(screen, bombeiros_vivos)

        if im.start_but.visible:
            screen.blit(im.START_IMG, (im.start_but.x, im.start_but.y))

        if im.up_but.visible:
            screen.blit(im.BUTTOM_UP_IMG, (im.up_but.x, im.up_but.y))
            screen.blit(im.BUTTOM_DOWN_IMG, (im.down_but.x, im.down_but.y))
            screen.blit(im.BUTTOM_LEFT_IMG, (im.left_but.x, im.left_but.y))
            screen.blit(im.BUTTOM_RIGHT_IMG, (im.right_but.x, im.right_but.y))
            screen.blit(im.BUTTOM_X_IMG, (im.x_but.x, im.x_but.y))

        if im.pause_but.visible:
            screen.blit(im.BUTTOM_PAUSE_IMG, (im.pause_but.x, im.pause_but.y))

        label.setText(f"Passos por segundo: {slider.getValue()}")
        pygame_widgets.update(events)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Gera o gráfico ao finalizar
    plt.plot(time_steps, alive_trees, label="Árvores Vivas")
    plt.plot(time_steps, burned_trees, label="Árvores Queimadas")
    plt.xlabel("Passos de Tempo")
    plt.ylabel("Número de Árvores")
    plt.title("Árvores Vivas vs Queimadas")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
