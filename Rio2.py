# Desenvolvido por Jader e Joênio
# Vou tentar refazer um prototipo(que fiz ontem) de rio que tenha um formato mais agradavel(sem ilhas e tentando não sair do mapa)
import random
import agents as agent
import images_but as im
import copy

"""def river_maker(matriz):
    pontos_x=[i for i in range(len(matriz[0]))]
    pontos_y=[i for i in range(len(matriz))]
    A=(random.choice(pontos_x),random.choice(pontos_y))
    B=(random.choice(pontos_x),random.choice(pontos_y))
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
        random.shuffle(passos)
        aqui_x= A[0]
        aqui_y= A[1]

        for i in passos:
            aqui_x+=i[0]
            aqui_y+=i[1]
            r=(aqui_x,aqui_y)
            rio.append(r)
    
    for i in pontos_y:
        start=False
        for j in pontos_x:
            if start:
                if (j,i) in rio:
                    start=False
                else:
                    rio.append((j,i))
                
            else:
              if (j,i) in rio:
                    start=True  
    return rio

if __name__=="__main__":
    matriz= [[0]*10 for _ in range(10)]
    for i in river_maker(matriz):
        matriz[i[1]][i[0]]=1
    print(matriz)

"""
def river_maker(matriz):
    pontos_x=[i for i in range(0, len(matriz))]
    pontos_y=[j for j in range(im.tela_x // im.cell_size //4, len(matriz[0]))]
    A=(random.choice(pontos_x),random.choice(pontos_y))
    B=(random.choice(pontos_x),random.choice(pontos_y))
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
    #print(A)
    #print(B)
    #print(passos)
    
    random.shuffle(passos)
    #print(passos)
    aqui_x= A[0]
    aqui_y= A[1]
    for i in passos:
        aqui_x+=i[0]
        aqui_y+=i[1]
        r=(aqui_x,aqui_y)
        rio.append(r)
    return rio
    
  
if __name__=="__main__":
    matriz= [[0]*10 for _ in range(10)]
    for i in river_maker(matriz):
        matriz[i[1]][i[0]]=1
    print(matriz)
