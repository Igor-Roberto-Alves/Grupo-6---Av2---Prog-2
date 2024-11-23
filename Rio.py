# Desenvolvido por Jader e Joênio

def river_maker(matriz):
    borda = []
    rio = []

    valores_de_x = range(len(matriz[0]))
    valores_de_y = range(len(matriz))

    A = (random.choice(valores_de_x), random.choice(valores_de_y))
    B = (random.choice(valores_de_x), random.choice(valores_de_y))

    dist = (A[0] - B[0], A[1] - B[1])

    Caminho = []
    aqui = A

    if dist[0] > 0:
        Caminho.extend([(1, 0)] * dist[0])
    else:
        Caminho.extend([(-1, 0)] * (-dist[0]))

    if dist[1] > 0:
        Caminho.extend([(0, 1)] * dist[1])
    else:
        Caminho.extend([(0, -1)] * (-dist[1]))

    for direcao in Caminho:
        aqui = (aqui[0] + direcao[0], aqui[1] + direcao[1])
        if 0 <= aqui[0] < len(matriz) and 0 <= aqui[1] < len(matriz[0]):
            borda.append(aqui)
            matriz[aqui[0]][aqui[1]] = agent.Barrier()  # Definir como um "barreira" (água)

    # Devolver a lista de células que compõem o rio
    return borda
