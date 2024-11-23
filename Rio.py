# Desenvolvido por Jader e Joênio

import random
import agents as agent


def river_maker(matriz):
    # Define usando as linhas da matriz
    num_rows = len(matriz)
    num_cols = len(matriz[0])

    # Onde inicia o rio
    x_start = random.randint(0, num_rows - 1)
    y_start = random.randint(0, num_cols - 1)

    # Teremos uma lista para armazenar as coordenadas do Rio
    rio = []
    visited = set() 

    x, y = x_start, y_start
    rio.append((x, y))
    visited.add((x, y))

    # Movimentos possíveis: para cima, para baixo, para a esquerda ou para a direita
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # direita, baixo, esquerda, cima

    while len(rio) < num_rows * num_cols:  # Vamos tentar expandir o rio até cobrir a floresta
        # Pega o último ponto do rio
        current_x, current_y = rio[-1]

        # Embaralha os movimentos para aleatoriedade
        random.shuffle(directions)

        moved = False
        for dx, dy in directions:
            # Calcula a nova posição
            new_x, new_y = current_x + dx, current_y + dy

            # Verifica se está dentro dos limites e se a célula não foi visitada
            if (0 <= new_x < num_rows and 0 <= new_y < num_cols) and (new_x, new_y) not in visited:
                rio.append((new_x, new_y))
                visited.add((new_x, new_y))
                moved = True
                break  # Se mover para uma nova célula, sai do loop

        # Se não conseguimos mover, o rio está "trancado", interrompemos
        if not moved:
            break

    return rio