import pygame
import time
import agents as agent
from forest import Forest
from Rio import river_maker
import images_but as im
import random

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
clock = pygame.time.Clock()


def draw_forest(screen, forest):

    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, agent.Bush):
                if cell.condition == "alive":
                    screen.blit(im.BUSH_IMG, (j * im.cell_size, i * im.cell_size))
                else:
                    screen.blit(im.BUSH_BURN_IMG, (j * im.cell_size, i * im.cell_size))
            elif isinstance(cell, agent.Tree):
                if cell.condition == "alive":
                    screen.blit(im.TREE_ALIVE_IMG, (j * im.cell_size, i * im.cell_size))
                elif cell.condition == "burning":
                    screen.blit(
                        im.TREE_BURNING_IMG, (j * im.cell_size, i * im.cell_size)
                    )
                elif cell.condition == "burned":
                    screen.blit(
                        im.TREE_BURNED_IMG, (j * im.cell_size, i * im.cell_size)
                    )
            elif isinstance(cell, agent.Barrier):
                screen.blit(im.WATER_IMG, (j * im.cell_size, i * im.cell_size))

            if cell == "v":
                pygame.draw.rect(
                    screen,
                    (95, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )
            if cell == "black":
                pygame.draw.rect(
                    screen,
                    (105, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )


def draw_rio(screen, borda, cell_size, map_width, map_height):
    for (x, y) in borda:
        # Verifica se as coordenadas estão dentro dos limites da tela
        if 0 <= x < map_height and 0 <= y < map_width:
            pygame.draw.rect(
                screen,
                (0, 0, 255),  # Azul para representar água
                (y * cell_size, x * cell_size, cell_size, cell_size),
            )



def draw_bombeiros(screen, lista_bombeiros):
    for bombeiro in lista_bombeiros:
        if bombeiro.status == "alive":
            screen.blit(
                im.FIREMAN_IMG, (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size)
            )
        if bombeiro.status == "burning":
            screen.blit(
                im.FIREMAN_BURNING2_IMG,
                (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
            )
        if bombeiro.status == "burning2":
            screen.blit(
                im.FIREMAN_BURNING1_IMG,
                (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
            )


def draw_animals(screen, animals):
    remaining_animals = []  # Para armazenar os animais restantes
    for animal in animals:

        if animal.status == "alive" and not animal.egg:
            screen.blit(
                im.CHICKEN_IMG, (animal.y * im.cell_size, animal.x * im.cell_size)
            )
            remaining_animals.append(animal)
        elif animal.status == "alive" and animal.egg:
            screen.blit(im.EGG_IMG, (animal.y * im.cell_size, animal.x * im.cell_size))
            remaining_animals.append(animal)
        elif animal.status == "dead":
            screen.blit(
                im.CHICKEN_DEAD_IMG, (animal.y * im.cell_size, animal.x * im.cell_size)
            )
            remaining_animals.append(animal)

    return remaining_animals


def draw_birds(screen, birds):
    for bird in birds:
        # Defina a cor roxa
        PURPLE = (128, 0, 128)

        # Tamanho do quadrado (em pixels)
        square_size = 8

        # Coordenadas do quadrado (ajustadas para o tamanho de célula)
        square_x = int(bird.y * im.cell_size)
        square_y = int(bird.x * im.cell_size)

        # Desenha o quadrado na tela
        pygame.draw.rect(screen, PURPLE, (square_x, square_y, square_size, square_size))


def init_screen():
    screen = pygame.display.set_mode((im.tela_x, im.tela_y))

    # Determinando a matriz com Bush (1/5), Tree (3/5) e "v" (1/5)
    matriz = [
        [
            random.choices(
                [agent.Bush((i, j)), agent.Tree((i, j)), "v"], weights=[1, 3, 6], k=1
            )[0]
            for j in range(im.tela_x // im.cell_size)
        ]
        for i in range(im.tela_y // im.cell_size)
    ]

    # Configurando uma área da matriz como "black"
    for i in range((im.tela_x // im.cell_size) // 4):
        for j in range(im.tela_y // im.cell_size):
            matriz[j][i] = "black"
    return matriz, screen


def main():

    matriz, screen = init_screen()
    forest = Forest(matriz)  # Inicializando a Floresta

    running = True
    start = False  # Controle para verificar se o incêndio deve iniciar
    start2 = False
    loading = False
    num_rios = 1
    num_fireman = 20
    rios = [river_maker(matriz)]
    bombeiros = [agent.bombeiro(matriz) for _ in range(num_fireman)]
    birds = [agent.Bird(matriz) for _ in range(10)]
    forest.surge_trees = False

    # Passos por segundo
    steps_by_second = 10
    TIMERSTEPEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMERSTEPEVENT, 1000 // steps_by_second)

    label = TextBox(screen, 15, 10, 270, 30, fontSize=20)
    label.setText(f"Passos por segundo: {steps_by_second}")
    label.disable()

    slider = Slider(
        screen, 20, 50, 250, 12, min=1, max=60, step=1, initial=steps_by_second
    )

    number_chickens = 10
    animals = [agent.Animal(matriz) for _ in range(number_chickens)]
    label2 = TextBox(screen, 15, 90, 270, 30, fontSize=20)
    label2.setText(f"Número de galinhas: {number_chickens}")
    label2.disable()
    label3 = TextBox(screen, 15, 170, 270, 30, fontSize=20)
    label3.setText(f"Número de bombeiros: {num_fireman}")
    label4 = TextBox(screen, 15, 250, 270, 30, fontSize=20)
    label4.setText(f"Número de rios: {num_rios}")


    slider_chicken = Slider(
        screen, 20, 130, 250, 12, min=1, max=200, step=1, initial=number_chickens
    )
    adding_chicken = False
    adding_fireman = False
    slider_fireman = Slider(
        screen, 20, 210, 250, 12, min=1, max=200, step=1, initial=num_fireman
    )
    slider_rio = Slider(
        screen, 20, 290, 250, 12, min=1, max=5, step=1, initial=num_rios
    )

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
                    im.start_but.visible = False  # Esconde o botão após o clique
                    start = True  # Inicia o incêndio após o clique
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
                if im.add_chicken_but.is_button_clicked(event.pos):
                    print("galinha clicada")
                    adding_chicken = True
                if im.add_fireman_but.is_button_clicked(event.pos):
                    print("bombeiro colocado")
                    adding_fireman = True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                grid_x = mouse_y // im.cell_size
                grid_y = mouse_x // im.cell_size
                if adding_chicken:
                    # Soltar o mouse para adicionar a galinha
                    if matriz[grid_x][grid_y] != "black":

                        animals.append(
                            agent.Animal(matriz, x=grid_x, y=grid_y)
                        )  # Adiciona galinha
                    adding_chicken = False

                elif adding_fireman:
                    if matriz[grid_x][grid_y] != "black":
                        bombeiros.append(agent.bombeiro(matriz, x=grid_x, y=grid_y))
                        adding_fireman = False

            elif event.type == TIMERSTEPEVENT:
                if start:
                    forest.incendio()  # Inicia o incêndio
                    start = False

                if loading:

                    forest.update_forest()

                    for bombeirx in bombeiros_vivos:
                        bombeirx.update_condition()

                    for animal in animals:
                        a = animal.update_condition()
                        if a:
                            animals.append(a)
                    if birds:
                        for bird in birds:
                            bird.update_condition()
                        birds[0].at_listbirds(birds)
                    else:
                        birds.append(agent.Bird(matriz))

        # Verifica se a velocidade foi alterada
        if slider.getValue() != steps_by_second:
            steps_by_second = slider.getValue()
            pygame.time.set_timer(TIMERSTEPEVENT, 1000 // steps_by_second)

        if slider_rio.getValue() != num_rios:
            num_rios = slider_rio.getValue()
            rios = [river_maker(matriz) for _ in range(num_rios)]

        if slider_chicken.getValue() != number_chickens:
            number_chickens = slider_chicken.getValue()
            animals = [agent.Animal(matriz) for _ in range(number_chickens)]
        if slider_fireman.getValue() != num_fireman:
            num_fireman = slider_fireman.getValue()
            bombeiros = [agent.bombeiro(matriz) for _ in range(num_fireman)]

        screen.fill((85, 107, 47))
        draw_forest(screen, forest)
        bombeiros_vivos = []
        for bomb in bombeiros:
            if bomb.status != "dead":
                bombeiros_vivos.append(bomb)

        draw_bombeiros(screen, bombeiros_vivos)
        animals = draw_animals(screen, animals)
        draw_birds(screen, birds)
        

        # Agora, chamando a função com os parâmetros necessários
        for rio in rios:
            draw_rio(screen, rio, im.cell_size, len(matriz[0]), len(matriz))


        # Desenhar o botão apenas se ele estiver visível
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

        if im.add_chicken_but.visible:

            overlay = pygame.Surface(
                (im.add_chicken_but.width, im.add_chicken_but.height)
            )
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (im.add_chicken_but.x, im.add_chicken_but.y))

            # Desenhar a imagem do botão depois
            # screen.blit(im.ADD_CHICKEN_IMG, (im.add_chicken_but.x, im.add_chicken_but.y))

        if im.add_fireman_but.visible:
            # Criar e desenhar o quadrado translúcido primeiro
            overlay = pygame.Surface(
                (im.add_fireman_but.width, im.add_fireman_but.height)
            )  # Dimensões do botão
            overlay.set_alpha(
                128
            )  # Define a transparência (0 totalmente transparente, 255 totalmente opaco)
            overlay.fill((0, 0, 0))  # Preenche a superfície com preto
            screen.blit(
                overlay, (im.add_fireman_but.x, im.add_fireman_but.y)
            )  # Desenhar a superfície translúcida

        label.setText(f"Passos por segundo: {slider.getValue()}")
        label2.setText(f"Número de galinhas: {slider_chicken.getValue()}")
        label3.setText(f"Número de bombeiros: {slider_fireman.getValue()}")
        pygame_widgets.update(events)

        pygame.display.flip()  # Atualiza a tela

        clock.tick(60)  # Limita o FPS a 60

    pygame.quit()


if __name__ == "__main__":
    main()