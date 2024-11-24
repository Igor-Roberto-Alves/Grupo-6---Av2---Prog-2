"""Infelizmente, foi tudo que consegui implementar (fora as coisas que fiz com o Jôenio). 
A ideia era ampliar esta função para gerar casas aleatoriamente — mantendo-as juntas para deixar algum nível de organização. 
Contudo, falta aplicar esta função na matriz(mapa) para gerar as casas propriamente ditas — falta também programar o mapa para desenhar 
as casas.  
Ademais, teoricamente, programar as barreiras para surgirem nas bordas da área (`city_area`) 
também não seria difícil.  Peço desculpa por não ter terminado até agora as coisas que fui incumbido de fazer, vou tentar terminar amanhã.
"""
import random
import muro

def city_area(matriz):
    """Define uma área aleatória na matriz."""
    pontos_x = range(len(matriz))
    pontos_y = range(len(matriz[0]))  
    pontos = [(i, j) for i in pontos_x for j in pontos_y]
    
    Centro = (random.choice(pontos_x), random.choice(pontos_y))
    h = random.choice(range(3)) + 1
    b = random.choice(range(3)) + 1
    
    area = []
    altura_max = min(Centro[1] + h, len(matriz) - 1)
    altura_min = max(Centro[1] - h, 0)
    largura_max = min(Centro[0] + b, len(matriz[0]) - 1)
    largura_min = max(Centro[0] - b, 0)
    
    for i in pontos:
        if largura_min <= i[0] <= largura_max and altura_min <= i[1] <= altura_max:
            area.append(i)
    
    return area

def houses(matriz, area):
    """Coloca casas em locais aleatórios dentro de uma área."""
    casinhas = []
    espaço = area.copy()  # Faz uma cópia da área para evitar alterações indesejadas
    
    num_casas = random.randint(1, len(espaço) // 2)
    for _ in range(num_casas):
        posicao = random.choice(espaço)
        espaço.remove(posicao)  # Remove a posição escolhida para evitar duplicatas
        casinhas.append(posicao)
    
    return casinhas



if __name__ == "__main__":
    matriz = [[0 for _ in range(10)] for _ in range(10)]
    area = city_area(matriz)
    for i in area:
        matriz[i[1]][i[0]] = 1 
    casas = houses(matriz, area)
    for i in casas:
        matriz[i[1]][i[0]] = 2  # Neste teste as casas são marcadas com um valor diferente (2)
    for linha in matriz:
        print(linha)

    #Criar Muros
    muro.criar_caminho(matriz)
    for linha in matriz:
        print(linha)