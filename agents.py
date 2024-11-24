import random


class Agent:
    # Todo agente carregará neighbors e update_condition
    def neighbors(self, matriz):
        lista = []
        directions = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                if isinstance(matriz[nx][ny], Tree) or isinstance(matriz[nx][ny], Bush):
                    lista.append(matriz[nx][ny])

        return lista

    def update_condition(self):
        raise NotImplementedError

    # O ideal ao criar um agente deve ser conter tudo que ele faz em update_condition
    # Assim facilitaria atualizar o agente a cada iteração


class Animal(Agent):
    def __init__(self, matriz, x=None, y=None, egg=False):
        self.matriz = matriz  # Matriz da floresta
        self.life = 1
        self.status = "alive"
        self.egg = egg  # A galinha está em forma de ovo ou já nasceu
        # Atributos auxiliares
        self.step = 0
        self.passo = 0
        self.morrendo = 0

        # O animal nasce em uma posição aleatória da floresta
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break

        # Se for passado x,y no caso do ovo
        if x and y:
            self.x = x
            self.y = y

    def bush_proximo(self):
        queue = [(self.x, self.y, 0)]  # Posição atual e distância inicial
        visited = set()
        visited.add((self.x, self.y))

        while queue:
            cx, cy, dist = queue.pop(0)

            # Verifica se a célula atual é um arbusto
            if isinstance(self.matriz[cx][cy], Bush):
                return cx, cy

            # Adiciona vizinhos à fila
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= nx < len(self.matriz)
                    and 0 <= ny < len(self.matriz[0])
                    and (nx, ny) not in visited
                    and isinstance(self.matriz[nx][ny], (Tree, Bush))
                ):
                    queue.append((nx, ny, dist + 1))
                    visited.add((nx, ny))

        return None

    def mover_para_bush(self):
        destino = self.bush_proximo()
        if destino:
            dx = destino[0] - self.x
            dy = destino[1] - self.y

            # Normaliza o movimento para andar apenas uma célula por vez
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)

            novo_x = self.x + dx
            novo_y = self.y + dy

            # Verifica se a nova posição é válida
            if (
                0 <= novo_x < len(self.matriz)
                and 0 <= novo_y < len(self.matriz[0])
                and isinstance(self.matriz[novo_x][novo_y], (Tree, Bush))
            ):
                self.x = novo_x
                self.y = novo_y
        else:
            self.andar()

    def update_life(self):
        # Se a galinha nao está em um arbusto ela está passando fome
        hungry = True
        lista_vizinhos = self.neighbors(self.matriz)
        lista_vizinhos.append(self.matriz[self.x][self.y])
        for neigh in lista_vizinhos:
            if isinstance(neigh, Bush):
                hungry = False  # Não está com fome se estiver em um arbusto
            if isinstance(neigh, Tree) or isinstance(
                neigh, Bush
            ):  # Se algum vizinho contando seu próprio lugar, estiver pegando fogo
                if neigh.condition == "burning":
                    self.life -= 0.1
                    if self.egg:  # Se for um ovo morre instantaneamente
                        self.life -= 1
        if hungry:  # A cada passo com fome perde 0.1 de vida
            self.life -= 0.1

        if self.life <= 0:
            self.status = "dead"
            if self.egg:
                self.status = "final"

    def update_condition(self):
        if isinstance(self.matriz[self.x][self.y],Bush):
            self.matriz[self.x][self.y].life -= 0.1

        if not self.egg and self.status != "dead" and self.status != "final":
            self.passo += 1
            if self.passo == 4:
                self.mover_para_bush()
                self.update_life()
                self.passo = 0
            return self.procriar()
        if self.status == "dead":
            self.morrendo += 1
            if self.morrendo == 100:

                self.status = "final"

        elif self.egg:
            self.step += 1
            self.update_life()
            if self.step == 20:
                self.egg = False
                self.life = 1


        return None

    def andar(self):

        direction = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        ]
        random.shuffle(direction)
        directions_possi = []
        for dx, dy in direction:
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= nx < len(self.matriz)
                and 0 <= ny < len(self.matriz[0])
                and (
                    isinstance(self.matriz[nx][ny], Tree) or self.matriz[nx][ny] == "v"
                )
            ):
                self.x, self.y = nx, ny  # Move o bombeiro para a nova posição
                directions_possi.append((nx, ny))

        if directions_possi:
            a = random.choice(directions_possi)
            self.x, self.y = a[0], a[1]

    def procriar(self):
        if self.status == "alive":
            a = random.randint(1, 200)  # Põem um ovo com esta probabilidade
            if a == 1:
                return Animal(self.matriz, self.x, self.y, True)




class Bird:
    def __init__(self, matrix, x=None, y=None):
        if x and y:
            self.x, self.y = x, y
        else:
            while True:
                self.x = random.randint(0, len(matrix) - 1)
                self.y = random.randint(0, len(matrix[0]) - 1)
                cell = matrix[self.x][self.y]
                if isinstance(cell, Tree):
                    break

        self.status = "alive"
        self.age = 0
        self.lifespan = random.randint(20, 50)
        self.matrix = matrix


    def move(self, distance=5):
        """
        Move o pássaro de acordo com a presença de fogo ou aleatoriamente.

        :param distance: Distância de detecção (sempre 1, pois só verifica células adjacentes).
        """
        if self.status != "alive":
            return  # Pássaros mortos não podem se mover.

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # Coordenadas das 8 células ao redor.
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Cima
            (0, -1),         (0, 1),     # Lados
            (1, -1), (1, 0), (1, 1)      # Baixo
        ]

        fire_detected = False
        safe_moves = []

        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                cell = self.matrix[nx][ny]
                if isinstance(cell, Tree) and cell.condition == "burning":
                    fire_detected = True
                    # Move para a direção oposta ao fogo.
                    opposite_x, opposite_y = self.x - dx, self.y - dy
                    if 0 <= opposite_x < rows and 0 <= opposite_y < cols:
                        self.x, self.y = opposite_x, opposite_y
                        # Verifica se a nova posição é inválida.
                        if self.matrix[self.x][self.y] == "black":
                            self.status = "dead"
                        return
                elif cell != "black":
                    safe_moves.append((nx, ny))

        # Se nenhum fogo for detectado, move para uma célula adjacente aleatória.
        if not fire_detected and safe_moves:
            self.x, self.y = random.choice(safe_moves)

        # Verifica se o pássaro saiu da matriz ou está em uma posição inválida.
        if not (0 <= self.x < rows and 0 <= self.y < cols) or self.matrix[self.x][self.y] == "black":
            self.status = "dead"

    def plant_tree(self, seed_prob=0.05, bush_prob=0.05):
        if self.status != "alive":
            return

        if self.matrix[self.x][self.y] == "v" and random.random() < seed_prob:
            self.matrix[self.x][self.y] = Tree([self.x, self.y])
        elif self.matrix[self.x][self.y] == "v" and random.random() < bush_prob:
            self.matrix[self.x][self.y] = Bush([self.x, self.y])


    def check_fire(self, fire_radius=1):
        if self.status != "alive":
            return False

        for dx in range(-fire_radius, fire_radius + 1):
            for dy in range(-fire_radius, fire_radius + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(self.matrix) and 0 <= ny < len(self.matrix[0]):
                    cell = self.matrix[nx][ny]
                    if isinstance(cell, Tree) and cell.condition == "burning":
                        self.status = "burning"
                        return True
        return False

    def reproduce(self, birds, mating_prob=0.1, max_birds=300):
        if len(birds) >= max_birds:
            return
        if (
            self.age >= 10
        ):  # O pássaro pode começar a se reproduzir após atingir certa idade
            # Verificar se há outros pássaros nas proximidades
            nearby_birds = [
                bird
                for bird in birds
                if abs(bird.x - self.x) <= 3
                and abs(bird.y - self.y) <= 3
                and bird != self
            ]
            if (
                nearby_birds and random.random() < mating_prob
            ):  # 10% de chance de reprodução
                # Gerar um novo pássaro em uma posição próxima
                new_bird = Bird(
                    self.matrix,
                    x=self.x + random.choice([-1, 0, 1]),
                    y=self.y + random.choice([-1, 0, 1]),
                )
                birds.append(new_bird)

    def update_condition(self, birds):
        if self.status == "dead":
            return

        self.move()
        self.plant_tree()
        self.reproduce(birds)
        self.age += 1

        if self.age >= self.lifespan:
            self.status = "dead"

    def at_listbirds(self, list_birds):
        list_birds[:] = [bird for bird in list_birds if bird.status != "dead"]


class Tree(Agent):
    def __init__(self, coord):
        self.condition = "alive"
        self.umidade = random.randint(80, 85)  # Resistência ao fogo baseada na umidade
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0  # Contador para etapas de queima
        self.step = 0  # Etapas que a árvore passa antes de ser "final"
        self.protect = None
        self.protectcount = 0

    def attempt_to_burn(self, matriz, vent):
        """
        Tenta propagar o fogo para os vizinhos com base na condição atual,
        umidade e influência do vento.
        """
        for neighbor in self.neighbors(matriz):
            if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                # Calcula a probabilidade base de queima
                base_probability = 100 - neighbor.umidade

                # Reduz a probabilidade se o fogo estiver se dissipando
                if self.condition == "burned":
                    base_probability -= 10  # Fogo menos intenso

                # Ajusta com base no vento
                if vent.directions:
                    if neighbor in vent.neighbors_vento(self, matriz):
                        base_probability = min(
                            90, base_probability + 30
                        )  # Aumenta devido ao vento
                        base_probability = 100
                    else:
                        base_probability = max(
                            10, base_probability - 20
                        )  # Reduz se fora da direção do vento
                        base_probability = 0

                # Probabilidade ajustada com um fator de suavização
                probability = max(
                    0, min(100, base_probability)
                )  # Garante limite entre 0 e 100

                # Tenta queimar o vizinho
                if random.random() < probability / 100:
                    neighbor.next_condition = "burning"

    def update_condition(self, forest):
        """
        Atualiza a condição da árvore com base no estado atual e propaga o fogo para os vizinhos.
        """
        matriz = forest.matriz
        vent = forest.vent

        if self.next_condition == "burned":
            self.condition = "burned"
            self.step += 1  # Passa um passo como "queimada"
            if self.step == 4:  # Após 3 etapas, marca como finalizada
                self.next_condition = "final"
            else:
                self.attempt_to_burn(matriz, vent)

        elif self.next_condition == "final":
            matriz[self.x][self.y] = "v"  # Some

        elif self.next_condition == "alive":
            if isinstance(self, Bush):
                matriz[self.x][self.y] = Bush([self.x, self.y])
            else:
                matriz[self.x][self.y] = Tree([self.x, self.y])

        elif self.next_condition == "burning":
            self.count += 1  # Incrementa o contador enquanto está queimando
            self.condition = self.next_condition
            if self.count == 2:
                self.attempt_to_burn(matriz, vent)  # Propaga o fogo para os vizinhos
            if self.count > 4:  # Queima por 2 etapas antes de ser marcada como "burned"
                self.next_condition = "burned"
        
    def __repr__(self):
        """
        Representação textual da árvore na matriz:
        - '1' para viva
        - 'b' para queimando
        - '0' para queimada
        """
        if self.condition == "alive":
            return "1"
        if self.condition == "burning":
            return "b"
        if self.condition == "burned":
            return "0"


class Bush(Tree):
    def __init__(self, coord):

        super().__init__(coord)
        self.umidade = random.randint(50, 60)  # Bushes têm umidade menor que árvores
        self.life = 1
    
    def update_condition(self, forest):
        if self.life <= 0:
            forest.matriz[self.x][self.y] = "v"
        return super().update_condition(forest)



class Rain:
    def __init__(self, matriz, intensity=50):
        """
        Essa classe recebe o valor intensidade e
        ativa a chuva que atua em toda a matriz.
        """
        self.matriz = matriz
        self.intensity = intensity

    def size_neighbors_rain(self):
        neighbors = []
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                cell = self.matriz[i][j]
                if cell != "black":
                    neighbors.append([i, j])
        return neighbors

    def rain_drop(self):
        neigh_drop = []  # vizinhança molhada
        for n in self.size_neighbors_rain():
            if random.randint(1, 100) < self.intensity:
                neigh_drop.append(n)
        return neigh_drop

    def update_condition(self):
        wet = self.rain_drop()  # lista de molhados
        self.size_neighbors_rain()  # definindo o tamanho da chuva
        for neighx, neighy in wet:
            cell = self.matriz[neighx][neighy]
            if isinstance(cell, Tree):
                cell.condition = "alive"
                cell.next_condition = "alive"
            elif isinstance(cell, Bush):
                cell.next_condition = "alive"
                cell.condition = "alive"


class bombeiro(Agent):
    def __init__(self, matriz, x=None, y=None):
        self.step = 0  # Definindo o numero de atualizações para o bombeiro andar
        self.matriz = matriz  # Matriz da floresta
        self.life = 1  # O bombeiro terá vida igual a 1 e perderá conforme as árvores ao seu redor pegam fogo
        self.status = "alive"

        # Posição aleatória em que o bombeiro nascerá
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break
        if x and y:
            self.x, self.y = x, y

    def update_condition(self):
        self.andar()  # O bomebiro anda
        # Verificando árvores que estão queimando
        self.apaga_fogo()
        for neigh in self.neighbors(self.matriz):
            if isinstance(neigh, Tree):
                if neigh.condition == "burning":
                    self.life -= 0.01

        if 0.5 <= self.life <= 0.8:
            self.status = "burning"

        elif 0 < self.life < 0.5:
            self.status = "burning2"

        elif self.life <= 0:
            self.status = "dead"

    def andar(self):
        # A função andar, por enquanto apenas leva o bombeiro para um vizinho aleatório
        self.step += 1
        if self.step == 5:
            direction = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
            ]
            random.shuffle(direction)
            directions_possi = []
            for dx, dy in direction:
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < len(self.matriz)
                    and 0 <= ny < len(self.matriz[0])
                    and (
                        isinstance(self.matriz[nx][ny], Tree)
                        or self.matriz[nx][ny] == "v"
                    )
                ):
                    self.x, self.y = nx, ny  # Move o bombeiro para a nova posição
                    directions_possi.append((nx, ny))

            if directions_possi:
                a = random.choice(directions_possi)
                self.x, self.y = a[0], a[1]

            self.step = 0

    def apaga_fogo(self):
        # Obtém os vizinhos ao redor do bombeiro
        neigh = self.neighbors(self.matriz)

        # Verifica a posição atual do bombeiro e adiciona à lista de vizinhos, se necessário
        if self.matriz[self.x][self.y] != "v":
            neigh.append(self.matriz[self.x][self.y])

        # Itera sobre os vizinhos
        for n in neigh:
            if isinstance(n, Tree):
                # Verifica se a árvore está no estágio "burning"
                if (
                    n.condition == "burning"
                ):  # Supondo que 'condition' seja o atributo que guarda o estado da árvore
                    # Apaga o fogo da árvore, criando uma nova árvore no estado saudável
                    self.matriz[n.x][n.y] = Tree([n.x, n.y])
                    break  # Apaga o fogo de apenas uma árvore de cada vez
            elif isinstance(n, Bush):
                # Verifica se o arbusto está no estágio "burning"
                if (
                    n.condition == "burning"
                ):  # Supondo que 'condition' seja o atributo que guarda o estado do arbusto
                    # Apaga o fogo do arbusto, criando um novo arbusto no estado saudável
                    self.matriz[n.x][n.y] = Bush([n.x, n.y])
                    break  # Apaga o fogo de apenas um arbusto de cada vez


class buttom:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.visible = True

    def is_button_clicked(self, pos):
        if self.visible:
            return (
                self.x <= pos[0] <= self.x + self.width
                and self.y <= pos[1] <= self.y + self.height
            )
        else:
            return None


class Barrier:  # representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return "a"


# Classe auxiliadora que representa
class H(Agent):
    def __init__(self, coord):
        self.x, self.y = coord

    def __repr__(self):
        return "H"


class House(Agent):
    def __init__(self, coord):

        self.condition = "safe"
        self.init = True

    def coords(self, matriz):
        """
        Define as coordenadas de um quadrado 3x3 ao redor do ponto central (x, y),
        ajustando o quadrado caso as coordenadas originais não sejam válidas.

        Retorna as coordenadas válidas ou None se não for possível encontrar um bloco 3x3 válido.
        """
        x, y = self.coord[0], self.coord[1]  # Coordenada inicial
        directions = [
            (0, 0),  # Centro (posição original)
            (0, 1),  # Deslocar para a direita
            (0, -1),  # Deslocar para a esquerda
            (1, 0),  # Deslocar para baixo
            (-1, 0),  # Deslocar para cima
            (1, 1),  # Diagonal inferior direita
            (1, -1),  # Diagonal inferior esquerda
            (-1, 1),  # Diagonal superior direita
            (-1, -1),  # Diagonal superior esquerda
        ]

        for dx, dy in directions:
            # Ajustar a posição central com base na direção
            nx, ny = x + dx, y + dy
            coords = [(nx + dx, ny + dy) for dx in range(-1, 2) for dy in range(-1, 2)]

            # Verificar se o bloco 3x3 na posição ajustada é válido
            valid = True
            for cx, cy in coords:
                if not (0 <= cx < len(matriz) and 0 <= cy < len(matriz[0])):
                    valid = False
                    break
                if matriz[cx][cy] == "black":
                    valid = False
                    break

            # Retorna as coordenadas válidas assim que encontrar
            if valid:
                return coords

        # Se nenhuma posição for válida, retorna None
        return None

    def check_neighbors(self, matriz):
        coordenadas_casa = self.coords()
        for coord in coordenadas_casa:
            coord.neighbors(matriz)
            for nx, ny in neighbors:
                if 0 <= nx < len(self.matriz) and 0 <= ny < len(self.matriz[0]):
                    neighbor = self.matriz[nx][ny]
                    if (
                        isinstance(neighbor, (Tree, Bush))
                        and neighbor.condition == "burning"
                    ):
                        self.life -= 0.01
                        return

    def check_life(self):
        if self.life <= 0:
            self.condition = "fim"

    def update_condition(self):
        self.check_neighbors()
        self.check_life()


class vento:
    def __init__(self, direction=None):
        lista_directions = ["N", "S", "L", "O", "NO", "NE", "SE", "SO"]
        self.directions = []
        if direction == 1:
            direction = random.choice(lista_directions)
        if direction == "L":
            self.directions = [(0, 1), (1, 1), (-1, 1)]
        elif direction == "O":
            self.directions = [(0, -1), (1, -1), (-1, -1)]
        elif direction == "S":
            self.directions = [(1, 0), (1, 1), (1, -1)]
        elif direction == "N":
            self.directions = [(-1, 0), (-1, 1), (-1, -1)]
        elif direction == "SE":
            self.directions = [(0, 1), (1, 0), (1, 1)]
        elif direction == "NE":
            self.directions = [(0, 1), (-1, 0), (-1, 1)]
        elif direction == "SO":
            self.directions = [(0, -1), (1, 0), (1, -1)]
        elif direction == "NO":
            self.directions = [(0, -1), (-1, 0), (-1, -1)]

    def neighbors_vento(self, tree, matriz):
        lista = []
        if self.directions:
            for dx, dy in self.directions:
                nx, ny = tree.x + dx, tree.y + dy
                if (
                    0 <= nx < len(matriz)
                    and 0 <= ny < len(matriz[0])
                    and isinstance(matriz[nx][ny], Tree)
                ):
                    lista.append(matriz[nx][ny])

        return lista

#Estaremos melhorando a implementação o quanto antes
class agua(Agent):
    def __init__(self,coord):
        self.x=coord[0]
        self.y=coord[1]

class River(Agent):
    def __init__(self, coord, matriz): 
        self.matriz = matriz
        self.aguas = []
        
        # Adiciona somente as coordenadas válidas
        for i in coord:
            x, y = i
            if 0 <= x < len(matriz) and 0 <= y < len(matriz[0]):  # Verifica se a coordenada está dentro dos limites da matriz
                self.aguas.append(agua(i))