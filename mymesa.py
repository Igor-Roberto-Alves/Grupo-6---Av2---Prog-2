import pygame
import time
import agents as ag
from forest import Floresta
import images_but as im
import random

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
relogio = pygame.time.Clock()


def desenhar_floresta(tela, floresta):

    for i in range(floresta.n):
        for j in range(floresta.m):
            celula = floresta.matriz[i][j]
            if isinstance(celula, ag.Arbusto):
                if celula.condiçao == "vivo":
                    tela.blit(im.ARBUSTO_IMG, (j * im.tamanho_celula, i * im.tamanho_celula))
                else:
                    tela.blit(im.ARBUSTO_QUEIMANDO_IMG, (j * im.tamanho_celula, i * im.tamanho_celula))
            elif isinstance(celula, ag.Arvore):
                if celula.condiçao == "vivo":
                    tela.blit(im.ARVORE_VIVA_IMG, (j * im.tamanho_celula, i * im.tamanho_celula))
                elif celula.condiçao == "queimando":
                    tela.blit(
                        im.ARVORE_QUEIMANDO_IMG, (j * im.tamanho_celula, i * im.tamanho_celula)
                    )
                elif celula.condiçao == "queimado":
                    tela.blit(
                        im.ARVORE_QUEIMADA_IMG, (j * im.tamanho_celula, i * im.tamanho_celula)
                    )
            elif isinstance(celula, ag.Barreira):
                tela.blit(im.AGUA_IMG, (j * im.tamanho_celula, i * im.tamanho_celula))
            elif isinstance(celula, ag.Casa):
                pygame.draw.rect(
                    tela,
                    (139, 69, 19),  # Cor marrom para a casa
                    (j * im.tamanho_celula, i * im.tamanho_celula, im.tamanho_celula, im.tamanho_celula),
                )

            if celula == "grama":
                pygame.draw.rect(
                    tela,
                    (95, 107, 47),
                    (j * im.tamanho_celula, i * im.tamanho_celula, im.tamanho_celula, im.tamanho_celula),
                )
            if celula == "preto":
                pygame.draw.rect(
                    tela,
                    (105, 107, 47),
                    (j * im.tamanho_celula, i * im.tamanho_celula, im.tamanho_celula, im.tamanho_celula),
                )


def desenhar_bombeiros(tela, lista_bombeiros):
    for bombeiro in lista_bombeiros:
        if bombeiro.status == "vivo":
            tela.blit(
                im.BOMBEIRO_IMG, (bombeiro.y * im.tamanho_celula, bombeiro.x * im.tamanho_celula)
            )
        if bombeiro.status == "queimando":
            tela.blit(
                im.BOMBEIRO_QUEIMANDO2_IMG,
                (bombeiro.y * im.tamanho_celula, bombeiro.x * im.tamanho_celula),
            )
        if bombeiro.status == "queimando2":
            tela.blit(
                im.BOMBEIRO_QUEIMANDO1_IMG,
                (bombeiro.y * im.tamanho_celula, bombeiro.x * im.tamanho_celula),
            )


def desenhar_animais(tela, animais):
    animais_restantes = []  # Para armazenar os animais restantes
    for animal in animais:

        if animal.status == "vivo" and not animal.ovo:
            tela.blit(
                im.GALINHA_TRAS_IMG, (animal.y * im.tamanho_celula, animal.x * im.tamanho_celula)
            )
            animais_restantes.append(animal)
        elif animal.status == "vivo" and animal.ovo:
            tela.blit(im.OVO_IMG, (animal.y * im.tamanho_celula, animal.x * im.tamanho_celula))
            animais_restantes.append(animal)
        elif animal.status == "morto":
            tela.blit(
                im.FRANGO_ASSADO_IMG, (animal.y * im.tamanho_celula, animal.x * im.tamanho_celula)
            )
            animais_restantes.append(animal)

    return animais_restantes


def desenhar_passaros(tela, passaros):
    for passaro in passaros:
        # Defina a cor roxa
        ROXO = (128, 0, 128)

        # Tamanho do quadrado (em pixels)
        tamanho_quadrado = 4

        # Coordenadas do quadrado (ajustadas para o tamanho de célula)
        quadrado_x = int(passaro.y * im.tamanho_celula)
        quadrado_y = int(passaro.x * im.tamanho_celula)

        # Desenha o quadrado na tela
        pygame.draw.rect(tela, ROXO, (quadrado_x, quadrado_y, tamanho_quadrado, tamanho_quadrado))


def init_tela():
    tela = pygame.display.set_mode((im.tela_x, im.tela_y))

    matriz = [
        [
            random.choices(
                [ag.Arbusto((i, j)), ag.Arvore((i, j)), "grama"],
                weights = [2, 3, 1],
                k=1,
            )[0]
            for j in range(im.tela_x // im.tamanho_celula)
        ]
        for i in range(im.tela_y // im.tamanho_celula)
    ]

    # Configurando uma área da matriz como "preto"
    for i in range((im.tela_x // im.tamanho_celula) // 4):
        for j in range(im.tela_y // im.tamanho_celula):
            matriz[j][i] = "preto"

    return matriz, tela


def main():

    matriz, tela = init_tela()
    floresta = Floresta(matriz)  # Inicializando a Floresta

    rodando = True
    começo = False  # Controle para verificar se o incêndio deve iniciar
    começo2 = False
    carregando = False
    numero_bombeiro = 20
    bombeiros = [ag.bombeiro(matriz) for _ in range(numero_bombeiro)]
    passaros = [ag.Passaro(matriz) for _ in range(150)]
    floresta.surgir_arvores = False

    # Passos por segundo
    passos_por_segundo = 10
    EVENTO_PASSO_SIMULACAO = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_PASSO_SIMULACAO, 1000 // passos_por_segundo)

    rotulo = TextBox(tela, 15, 10, 270, 30, fontSize=20)
    rotulo.setText(f"Passos por segundo: {passos_por_segundo}")
    rotulo.disable()

    botao_deslizante = Slider(
        tela, 20, 50, 250, 12, min=1, max=60, step=1, inicial=passos_por_segundo
    )

    numero_galinhas = 10
    animais = [ag.Animal(matriz) for _ in range(numero_galinhas)]
    rotulo2 = TextBox(tela, 15, 90, 270, 30, fontSize=20)
    rotulo2.setText(f"Número de galinhas: {numero_galinhas}")
    rotulo2.disable()
    rotulo3 = TextBox(tela, 15, 170, 270, 30, fontSize=20)
    rotulo3.setText(f"Número de bombeiros: {numero_bombeiro}")

    botao_deslizante_galinha = Slider(
        tela, 20, 130, 250, 12, min=1, max=200, step=1, inicial=numero_galinhas
    )
    adicionando_galinha = False
    adicionando_bombeiro = False
    botao_deslizante_bombeiro = Slider(
        tela, 20, 210, 250, 12, min=1, max=1000, step=1, inicial=numero_bombeiro
    )

    while rodando:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if im.botao_start.esta_clicado(evento.pos) and im.botao_start.visivel:
                    if começo2:
                        carregando = True

                    print("Botão clicado!")
                    im.botao_start.visivel = False  # Esconde o botão após o clique
                    começo = True  # Inicia o incêndio após o clique
                    im.botao_pause.visivel = True
                    bombeiros_andar = True
                    carregando = True

                if im.botao_cima.esta_clicado(evento.pos):
                    print("up clicado")
                    floresta.vent = ag.vento("N")

                if im.botao_baixo.esta_clicado(evento.pos):
                    print("down clicado")
                    floresta.vent = ag.vento("S")

                if im.botao_direita.esta_clicado(evento.pos):
                    print("right clicado")
                    floresta.vent = ag.vento("L")

                if im.botao_esquerda.esta_clicado(evento.pos):
                    print("left clicado")
                    floresta.vent = ag.vento("O")

                if im.botao_de_x.esta_clicado(evento.pos):
                    print("x clicado")
                    floresta.vent = ag.vento()

                if im.botao_pause.esta_clicado(evento.pos):
                    print("pause clicado")
                    im.botao_start.visivel = True
                    im.botao_pause.visivel = False
                    começo2 = True
                    carregando = False
                if im.botao_adicionar_galinha.esta_clicado(evento.pos):
                    print("galinha clicada")
                    adicionando_bombeiro = True
                if im.botao_adicionar_bombeiros.esta_clicado(evento.pos):
                    print("bombeiro colocado")
                    adicionando_bombeiro = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = evento.pos
                grade_x = mouse_y // im.tamanho_celula
                grade_y = mouse_x // im.tamanho_celula
                if adicionando_galinha:
                    # Soltar o mouse para adicionar a galinha
                    if matriz[grade_x][grade_y] != "preto":

                        animais.append(
                            ag.Animal(matriz, x=grade_x, y=grade_y)
                        )  # Adiciona galinha
                    adicionando_galinha = False

                elif adicionando_bombeiro:
                    if matriz[grade_x][grade_y] != "preto":
                        bombeiros.append(ag.bombeiro(matriz, x=grade_x, y=grade_y))
                        adicionando_bombeiro = False

            elif evento.type == EVENTO_PASSO_SIMULACAO:
                if começo:
                
                    começo = False

                if carregando:

                    floresta.atualizar_floresta()

                    for bombeiro in bombeiros_vivos:
                        bombeiro.condiçao_de_atualizaçao()

                    for animal in animais:
                        a = animal.condiçao_de_atualizaçao()
                        if a:
                            animais.append(a)
                    if passaros:
                        for passaro in passaros:
                            passaro.condiçao_de_atualizaçao(passaros)
                        passaros[0].atualizar_populacao_de_passaros(passaros)
                    else:
                        passaros.append(ag.Passaro(matriz))

        # Verifica se a velocidade foi alterada
        if botao_deslizante.getValue() != passos_por_segundo:
            passos_por_segundo = botao_deslizante.getValue()
            pygame.time.set_timer(EVENTO_PASSO_SIMULACAO, 1000 // passos_por_segundo)

        if botao_deslizante_galinha.getValue() != numero_galinhas:
            numero_galinhas = botao_deslizante_galinha.getValue()
            animais = [ag.Animal(matriz) for _ in range(numero_galinhas)]
        if botao_deslizante_bombeiro.getValue() != numero_bombeiro:
            numero_bombeiro = botao_deslizante_bombeiro.getValue()
            bombeiros = [ag.bombeiro(matriz) for _ in range(numero_bombeiro)]

        tela.fill((85, 107, 47))
        desenhar_floresta(tela, floresta)
        bombeiros_vivos = []
        for bombeiro in bombeiros:
            if bombeiro.status != "morto":
                bombeiros_vivos.append(bombeiro)

        desenhar_bombeiros(tela, bombeiros_vivos)
        animais = desenhar_animais(tela, animais)
        desenhar_passaros(tela, passaros)

        # Desenhar o botão apenas se ele estiver visível
        if im.botao_start.visivel:
            tela.blit(im.BOTAO_START_IMG, (im.botao_start.x, im.botao_start.y))

        if im.botao_cima.visivel:
            tela.blit(im.BOTAO_CIMA_IMG, (im.botao_cima.x, im.botao_cima.y))
            tela.blit(im.BOTAO_BAIXO_IMG, (im.botao_baixo.x, im.botao_baixo.y))
            tela.blit(im.BOTAO_ESQUERDA_IMG, (im.botao_esquerda.x, im.botao_esquerda.y))
            tela.blit(im.BOTAO_DIREITA_IMG, (im.botao_direita.x, im.botao_direita.y))
            tela.blit(im.BOTAO_DE_X_IMG, (im.botao_de_x.x, im.botao_de_x.y))

        if im.botao_pause.visivel:
            tela.blit(im.BOTAO_PAUSE_IMG, (im.botao_pause.x, im.botao_pause.y))

        if im.botao_adicionar_galinha.visivel:

            sobreposiçao = pygame.Surface(
                (im.botao_adicionar_galinha.largura, im.botao_adicionar_galinha.altura)
            )
            sobreposiçao.set_alpha(128)
            sobreposiçao.fill((0, 0, 0))
            tela.blit(sobreposiçao, (im.botao_adicionar_galinha.x, im.botao_adicionar_galinha.y))

            # Desenhar a imagem do botão depois
            # tela.blit(im.ADD_CHICKEN_IMG, (im.add_chicken_but.x, im.add_chicken_but.y))

        if im.botao_adicionar_bombeiros.visivel:
            # Criar e desenhar o quadrado translúcido primeiro
            sobreposiçao = pygame.Surface(
                (im.botao_adicionar_bombeiros.largura, im.botao_adicionar_bombeiros.altura)
            )  # Dimensões do botão
            sobreposiçao.set_alpha(
                128
            )  # Define a transparência (0 totalmente transparente, 255 totalmente opaco)
            sobreposiçao.fill((0, 0, 0))  # Preenche a superfície com preto
            tela.blit(
                sobreposiçao, (im.botao_adicionar_bombeiros.x, im.botao_adicionar_bombeiros.y)
            )  # Desenhar a superfície translúcida

        # Carros de bombeiros

        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 100))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (325, 125))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (345, 150))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 175))

        tela.blit(im.CARRO_BOMBEIRO_IMG, (345, 275))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 300))
        
        tela.blit(im.CARRO_BOMBEIRO_IMG, (325, 400))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (345, 425))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 450))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (325, 475))

        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 550))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (325, 575))
        
        tela.blit(im.CARRO_BOMBEIRO_IMG, (345, 675))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (335, 700))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (345, 725))
        tela.blit(im.CARRO_BOMBEIRO_IMG, (325, 750))
        
        rotulo.setText(f"Passos por segundo: {botao_deslizante.getValue()}")
        rotulo2.setText(f"Número de galinhas: {botao_deslizante_galinha.getValue()}")
        rotulo3.setText(f"Número de bombeiros: {botao_deslizante_bombeiro.getValue()}")
        pygame_widgets.update(eventos)

        pygame.display.flip()  # Atualiza a tela

        relogio.tick(60)  # Limita o FPS a 60

    pygame.quit()


if __name__ == "__main__":
    main()
