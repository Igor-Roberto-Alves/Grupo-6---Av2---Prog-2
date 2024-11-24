import pygame
import os
import agents as agent

pygame.init()

size_of_w = pygame.display.get_desktop_sizes()
tela_x = int(size_of_w[0][0])
tela_y = int(size_of_w[0][1])
CARRO_BOMBEIRO_IMG = pygame.image.load(
    os.path.join("images", "carro_bombeiros (1).png")
)
CHICKEN_DEAD_IMG = pygame.image.load(
    os.path.join("images", "Cooked_Chicken_JE3_BE3.png")
)
CHUVA_BUT_IMG = pygame.image.load(os.path.join("images", "chuva_.png"))
ADD_CHICKEN_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (13).png"))
EGG_IMG = pygame.image.load(os.path.join("images", "egg.png"))
BUSH_BURN_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (12).png"))
BUSH_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (11).png"))
CHICKEN_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (10).png"))
TREE_ALIVE_IMG = pygame.image.load(os.path.join("images", "Tree_Small.png"))
TREE_BURNING_IMG = pygame.image.load(os.path.join("images", "Fire_Small.png"))
WATER_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (2).png"))
START_IMG = pygame.image.load(os.path.join("images", "shadedDark42.png"))
TREE_BURNED_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (4).png"))
BUTTOM_UP_IMG = pygame.image.load(os.path.join("images", "shadedDark03.png"))
BUTTOM_LEFT_IMG = pygame.image.load(os.path.join("images", "shadedDark05.png"))
BUTTOM_DOWN_IMG = pygame.image.load(os.path.join("images", "shadedDark10.png"))
BUTTOM_RIGHT_IMG = pygame.image.load(os.path.join("images", "shadedDark06.png"))
BUTTOM_X_IMG = pygame.image.load(os.path.join("images", "shadedDark35.png"))
BUTTOM_PAUSE_IMG = pygame.image.load(os.path.join("images", "shadedDark44.png"))
FIREMAN_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (5).png"))
FIREMAN_BURNING2_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (8).png")
)
FIREMAN_BURNING1_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (9).png")
)

but_size = tela_x // 80
cell_size = tela_x // 150
CHUVA_BUT_IMG = pygame.transform.scale(
    CHUVA_BUT_IMG, (CHUVA_BUT_IMG.get_width() // 2, CHUVA_BUT_IMG.get_height() // 2)
)
CARRO_BOMBEIRO_IMG = pygame.transform.scale(
    CARRO_BOMBEIRO_IMG,
    (CARRO_BOMBEIRO_IMG.get_width() // 80, CARRO_BOMBEIRO_IMG.get_height() // 80),
)
ADD_CHICKEN_IMG = pygame.transform.scale(
    ADD_CHICKEN_IMG, (4 * cell_size, 4 * cell_size)
)
CHICKEN_DEAD_IMG = pygame.transform.scale(CHICKEN_DEAD_IMG, (cell_size, cell_size))
EGG_IMG = pygame.transform.scale(EGG_IMG, (0.5 * cell_size, 0.5 * cell_size))
BUSH_BURN_IMG = pygame.transform.scale(BUSH_BURN_IMG, (cell_size, cell_size))
BUSH_IMG = pygame.transform.scale(BUSH_IMG, (cell_size, cell_size))
CHICKEN_IMG = pygame.transform.scale(CHICKEN_IMG, (1.5 * cell_size, 1.5 * cell_size))
TREE_ALIVE_IMG = pygame.transform.scale(TREE_ALIVE_IMG, (cell_size, cell_size))
TREE_BURNING_IMG = pygame.transform.scale(TREE_BURNING_IMG, (cell_size, cell_size))
WATER_IMG = pygame.transform.scale(WATER_IMG, (cell_size, cell_size))
TREE_BURNED_IMG = pygame.transform.scale(TREE_BURNED_IMG, (cell_size, cell_size))
BUTTOM_UP_IMG = pygame.transform.scale(BUTTOM_UP_IMG, (1.5 * but_size, 1.5 * but_size))
BUTTOM_LEFT_IMG = pygame.transform.scale(
    BUTTOM_LEFT_IMG, (1.5 * but_size, 1.5 * but_size)
)
BUTTOM_DOWN_IMG = pygame.transform.scale(
    BUTTOM_DOWN_IMG, (1.5 * but_size, 1.5 * but_size)
)
BUTTOM_RIGHT_IMG = pygame.transform.scale(
    BUTTOM_RIGHT_IMG, (1.5 * but_size, 1.5 * but_size)
)
BUTTOM_X_IMG = pygame.transform.scale(BUTTOM_X_IMG, (1.5 * but_size, 1.5 * but_size))
FIREMAN_IMG = pygame.transform.scale(FIREMAN_IMG, (1.5 * cell_size, 1.5 * cell_size))
FIREMAN_BURNING1_IMG = pygame.transform.scale(
    FIREMAN_BURNING1_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
FIREMAN_BURNING2_IMG = pygame.transform.scale(
    FIREMAN_BURNING2_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
START_IMG = pygame.transform.scale(START_IMG, (4 * but_size, 2 * but_size))
BUTTOM_PAUSE_IMG = pygame.transform.scale(
    BUTTOM_PAUSE_IMG, (4 * but_size, 2 * but_size)
)

add_fireman_but = agent.buttom(280, 200, 20, 20)

button_width, button_height = START_IMG.get_width(), START_IMG.get_height()
button_x, button_y = tela_x // 2, tela_y // 2
start_but = agent.buttom(button_x, button_y, button_width, button_height)

button_x, button_y = tela_x // 10, 0.42 * tela_y + 80
button_width, button_height = BUTTOM_UP_IMG.get_width(), BUTTOM_UP_IMG.get_height()
up_but = agent.buttom(button_x, button_y, button_width, button_height)

button_y = 0.525 * tela_y + 80
down_but = agent.buttom(button_x, button_y, button_width, button_height)
button_x = 0.07 * tela_x
button_y = 0.475 * tela_y + 80
left_but = agent.buttom(button_x, button_y, button_width, button_height)
button_x = 0.13 * tela_x
right_but = agent.buttom(button_x, button_y, button_width, button_height)
button_x = 0.1 * tela_x
x_but = agent.buttom(button_x, button_y, button_width, button_height)
button_x, button_y = 0.0035 * tela_x * cell_size, 0.025 * tela_y * cell_size
button_width, button_height = (
    BUTTOM_PAUSE_IMG.get_width(),
    BUTTOM_PAUSE_IMG.get_height(),
)
pause_but = agent.buttom(button_x, button_y + 400, button_width, button_height)
add_chicken_but = agent.buttom(280, 80, 20, 20)
init_rain_but = agent.buttom(
    300, 331, CHUVA_BUT_IMG.get_width(), CHUVA_BUT_IMG.get_height()
)
