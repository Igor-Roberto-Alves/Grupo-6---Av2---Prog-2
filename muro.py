import Vila
import random




'''
Achar os pontos ao redor da vila
'''

def pontos_ao_redor(matriz, valor, raio=1):
    pontos_encontrados = []
    pontos_ao_redor = []

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] in valor:
                pontos_encontrados.append((i, j))

    for ponto in pontos_encontrados:
        x, y = ponto
        for dx in range(-raio, raio+1):
            for dy in range(-raio, raio+1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]) and (nx != x or ny != y):
                    pontos_ao_redor.append((nx, ny))
    
    n_pontos = []
    for n in pontos_ao_redor:
        if matriz[n[0]][n[1]] == 0:
            n_pontos.append(n)
    
    return n_pontos


#Escolher 2 pontos aleatorios ao redor da vila e fazer um muro que os liga


import random

def caminho_entre_dois_pontos(p1, p2):

    caminho_parcial = []
    x1, y1 = p1
    x2, y2 = p2
    
    while x1 != x2:
        if x1 < x2:
            x1 += 1
        else:
            x1 -= 1
        caminho_parcial.append((x1, y1))
    
    while y1 != y2:
        if y1 < y2:
            y1 += 1
        else:
            y1 -= 1
        caminho_parcial.append((x1, y1))
    
    return caminho_parcial

def escolher_pontos_aleatorios(lista_pontos, num_pontos=2):
    return random.sample(lista_pontos, num_pontos)

def caminho_restrito(lista_pontos):


    n = True
    while n:
        pontos_aleatorios = escolher_pontos_aleatorios(lista_pontos)
        if pontos_aleatorios[0] != pontos_aleatorios[1]:
            break
    print(f"Pontos aleatórios escolhidos: {pontos_aleatorios}")
    
    ponto_inicial = pontos_aleatorios[0]
    ponto_final = pontos_aleatorios[1]

    caminho = [ponto_inicial]

    lista_pontos_sorted = sorted(lista_pontos, key=lambda p: (p[0], p[1]))

    caminho.extend(caminho_entre_dois_pontos(ponto_inicial, ponto_final))
    
    return caminho

def criar_caminho(matriz):
    pontos_ao_redor_1_2 = pontos_ao_redor(matriz, [1,2])
    p = list(set(pontos_ao_redor_1_2))
    print(p)
    pontos = caminho_restrito(p)
    for x, y in pontos:
        matriz[x][y] = 7



if __name__ == "__main__":
    matriz = [[0 for _ in range(10)] for _ in range(10)]
    area = Vila.city_area(matriz)
    for i in area:
        matriz[i[1]][i[0]] = 1 
    casas = Vila.houses(matriz, area)
    for i in casas:
        matriz[i[1]][i[0]] = 2  # Casas marcadas com 2
    for linha in matriz:
        print(linha)
    
    print("Pontos ao redor dos pontos 1 e 2:")
    criar_caminho(matriz)
    
    for linha in matriz:
        print(linha)