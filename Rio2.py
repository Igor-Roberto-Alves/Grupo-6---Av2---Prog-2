# Desenvolvido por Jader e Joênio
# Vou tentar refazer um prototipo(que fiz ontem) de rio que tenha um formato mais agradavel(sem ilhas e tentando não sair do mapa)
import random
import agents as agent
import copy

def river_maker(matriz):
    pontos_x=[i for i in range(matriz[0])]
    pontos_y=[i for i in range(matriz)]
    A=(random.choice(pontos_x,random.choice(pontos_y)))
    B=(random.choice(pontos_x,random.choice(pontos_y)))
    passos=[]
    rio=[A]
    delta_x = B[0] - A[0]
    delta_y = B[1] - A[1]
    # Movendo-se ao longo do eixo X
    if delta_x > 0:
        passos.extend([(1, 0)] * delta_x)  # Move para a direita
    elif delta_x < 0:
        passos.extend([(-1, 0)] * abs(delta_x))  # Move para a esquerda
    # Movendo-se ao longo do eixo Y
    if delta_y > 0:
        passos.extend([(0, 1)] * delta_y)  # Move para cima
    elif delta_y < 0:
        passos.extend([(0, -1)] * abs(delta_y))  # Move para baixo

    for _ in range(2): #faz duas fazes
        este_caminho= random.choice(passos.copy())
        aqui= A

        for i in este_caminho:
            aqui=(aqui[0]+i[0],aqui[1]+i[1])
            rio.append(aqui)
    
    for i in range(matriz):
        start=False
        for j in range(i):
            if start:
                if matriz[i][j]

            
