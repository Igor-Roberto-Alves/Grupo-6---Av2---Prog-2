import pygame
import os
import agents as ag

pygame.init()

tamanho_da_tela = pygame.display.get_desktop_sizes()
tela_x = int(tamanho_da_tela[0][0])
tela_y = int(tamanho_da_tela[0][1])
CARRO_BOMBEIRO_IMG = pygame.image.load(
    os.path.join("images", "carro_bombeiros (1).png")
)
FRANGO_ASSADO_IMG = pygame.image.load(
    os.path.join("images", "Cooked_Chicken_JE3_BE3.png")
)
GALINHA_FRENTE_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (13).png"))
OVO_IMG = pygame.image.load(os.path.join("images", "egg.png"))
ARBUSTO_QUEIMANDO_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (12).png"))
ARBUSTO_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (11).png"))
GALINHA_TRAS_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (10).png"))
ARVORE_VIVA_IMG = pygame.image.load(os.path.join("images", "Tree_Small.png"))
ARVORE_QUEIMANDO_IMG = pygame.image.load(os.path.join("images", "Fire_Small.png"))
AGUA_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (2).png"))
BOTAO_START_IMG = pygame.image.load(os.path.join("images", "shadedDark42.png"))
ARVORE_QUEIMADA_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (4).png"))
BOTAO_CIMA_IMG = pygame.image.load(os.path.join("images", "shadedDark03.png"))
BOTAO_ESQUERDA_IMG = pygame.image.load(os.path.join("images", "shadedDark05.png"))
BOTAO_BAIXO_IMG = pygame.image.load(os.path.join("images", "shadedDark10.png"))
BOTAO_DIREITA_IMG = pygame.image.load(os.path.join("images", "shadedDark06.png"))
BOTAO_DE_X_IMG = pygame.image.load(os.path.join("images", "shadedDark35.png"))
BOTAO_PAUSE_IMG = pygame.image.load(os.path.join("images", "shadedDark44.png"))
BOMBEIRO_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (5).png"))
BOMBEIRO_QUEIMANDO2_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (8).png")
)
BOMBEIRO_QUEIMANDO1_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (9).png")
)

tamanho_botao = tela_x // 80
tamanho_celula = tela_x // 150
CARRO_BOMBEIRO_IMG = pygame.transform.scale(
    CARRO_BOMBEIRO_IMG,
    (CARRO_BOMBEIRO_IMG.get_width() // 80, CARRO_BOMBEIRO_IMG.get_height() // 80),
)
GALINHA_FRENTE_IMG = pygame.transform.scale(
    GALINHA_FRENTE_IMG, (4 * tamanho_celula, 4 * tamanho_celula)
)
FRANGO_ASSADO_IMG = pygame.transform.scale(FRANGO_ASSADO_IMG, (tamanho_celula, tamanho_celula))
OVO_IMG = pygame.transform.scale(OVO_IMG, (0.5 * tamanho_celula, 0.5 * tamanho_celula))
ARBUSTO_QUEIMANDO_IMG = pygame.transform.scale(ARBUSTO_QUEIMANDO_IMG, (tamanho_celula, tamanho_celula))
ARBUSTO_IMG = pygame.transform.scale(ARBUSTO_IMG, (tamanho_celula, tamanho_celula))
GALINHA_TRAS_IMG = pygame.transform.scale(GALINHA_TRAS_IMG, (1.5 * tamanho_celula, 1.5 * tamanho_celula))
ARVORE_VIVA_IMG = pygame.transform.scale(ARVORE_VIVA_IMG, (tamanho_celula, tamanho_celula))
ARVORE_QUEIMANDO_IMG = pygame.transform.scale(ARVORE_QUEIMANDO_IMG, (tamanho_celula, tamanho_celula))
AGUA_IMG = pygame.transform.scale(AGUA_IMG, (tamanho_celula, tamanho_celula))
ARVORE_QUEIMADA_IMG = pygame.transform.scale(ARVORE_QUEIMADA_IMG, (tamanho_celula, tamanho_celula))
BOTAO_CIMA_IMG = pygame.transform.scale(BOTAO_CIMA_IMG, (1.5 * tamanho_botao, 1.5 * tamanho_botao))
BOTAO_ESQUERDA_IMG = pygame.transform.scale(
    BOTAO_ESQUERDA_IMG, (1.5 * tamanho_botao, 1.5 * tamanho_botao)
)
BOTAO_BAIXO_IMG = pygame.transform.scale(
    BOTAO_BAIXO_IMG, (1.5 * tamanho_botao, 1.5 * tamanho_botao)
)
BOTAO_DIREITA_IMG = pygame.transform.scale(
    BOTAO_DIREITA_IMG, (1.5 * tamanho_botao, 1.5 * tamanho_botao)
)
BOTAO_DE_X_IMG = pygame.transform.scale(BOTAO_DE_X_IMG, (1.5 * tamanho_botao, 1.5 * tamanho_botao))
BOMBEIRO_IMG = pygame.transform.scale(BOMBEIRO_IMG, (1.5 * tamanho_celula, 1.5 * tamanho_celula))
BOMBEIRO_QUEIMANDO1_IMG = pygame.transform.scale(
BOMBEIRO_QUEIMANDO1_IMG, (1.5 * tamanho_celula, 1.5 * tamanho_celula)
)
BOMBEIRO_QUEIMANDO2_IMG = pygame.transform.scale(
    BOMBEIRO_QUEIMANDO2_IMG, (1.5 * tamanho_celula, 1.5 * tamanho_celula)
)
BOTAO_START_IMG = pygame.transform.scale(BOTAO_START_IMG, (4 * tamanho_botao, 2 * tamanho_botao))
BOTAO_PAUSE_IMG = pygame.transform.scale(
    BOTAO_PAUSE_IMG, (4 * tamanho_botao, 2 * tamanho_botao)
)

botao_adicionar_bombeiros = ag.Botao(280, 200, 20, 20)

largura_botao, altura_botao = BOTAO_START_IMG.get_width(), BOTAO_START_IMG.get_height()
botao_x, botao_y = tela_x // 2, tela_y // 2
botao_start = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)

botao_x, botao_y = tela_x // 10, 0.42 * tela_y
largura_botao, altura_botao = BOTAO_CIMA_IMG.get_width(), BOTAO_CIMA_IMG.get_height()
botao_cima = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)

botao_y = 0.525 * tela_y
botao_baixo = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)
botao_x = 0.07 * tela_x
botao_y = 0.475 * tela_y
botao_esquerda = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)
botao_x = 0.13 * tela_x
botao_direita = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)
botao_x = 0.1 * tela_x
botao_de_x = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)
botao_x, botao_y = 0.003 * tela_x * tamanho_celula, 0.03 * tela_y * tamanho_celula
largura_botao, altura_botao = (
    BOTAO_PAUSE_IMG.get_width(),
    BOTAO_PAUSE_IMG.get_height(),
)
botao_pause = ag.Botao(botao_x, botao_y, largura_botao, altura_botao)
botao_adicionar_galinha = ag.Botao(280, 80, 20, 20)
