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
        self.matriz = matriz
        self.life = 1
        self.status = "alive"
        self.egg = egg
        self.step = 0
        self.passo = 0
        self.morrendo = 0

        # O animal nasce em uma posição aleatória
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break

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
        hungry = True
        for neigh in self.neighbors(self.matriz):
            if isinstance(neigh, Bush):
                hungry = False
            if isinstance(neigh, Tree):
                if neigh.condition == "burning":
                    self.life -= 0.1
                    if self.egg:
                        self.life -= 0.2
        if hungry:
            self.life -= 0.1

        if self.life <= 0:
            self.status = "dead"
            if self.egg:
                self.status = "final"

    def update_condition(self):
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
            a = random.randint(1, 200)
            if a == 1:
                return Animal(self.matriz, self.x, self.y, True)


class Bird:
    def __init__(self, matriz, x=None, y=None):
        self.matriz = matriz
        self.condition = "alive"
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break

        if x and y:
            self.x = x
            self.y = y
        self.spread_prob = 1  # Chance de semear uma árvore.
        self.step = 0

    def update_condition(self):
        self.step += 1
        if self.step == 3:
            dx, dy = random.randint(-2, 2), random.randint(-2, 2)
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(self.matriz) and 0 <= ny < len(self.matriz[0]):
                self.x, self.y = nx, ny
                if self.matriz[nx][ny] == "v" and random.random() < self.spread_prob:
                    b = random.randint(1, 3)
                    if b == 1:
                        self.matriz[nx][ny] = Tree([nx, ny])
                    else:
                        self.matriz[nx][ny] = Bush([nx, ny])
                elif self.matriz[nx][ny] == "black":
                    self.condition = "remove"
            else:
                self.condition = "remove"
            self.step = 0

    def at_listbirds(self, list_birds):
        for bird in list_birds:
            if bird.condition == "remove":
                list_birds.remove(bird)

        a = random.randint(0, 10)
        if a == 1:
            list_birds.append(Bird(self.matriz))


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
        neigh = self.neighbors(self.matriz)
        if self.matriz[self.x][self.y] != "v":
            neigh.append(self.matriz[self.x][self.y])
            print(self.matriz[self.x][self.y])
        for n in neigh:
            if isinstance(n, Tree):
                self.matriz[n.x][n.y] = Tree([n.x, n.y])
                break
            else:
                self.matriz[n.x][n.y] = Bush([n.x, n.y])
                break


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


class Tree(Agent):
    def __init__(self, coord):
        self.condition = "alive"
        self.density = random.randint(80, 90)
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0
        self.step = 0

    def attempt_to_burn(self, matriz, vent):
        for neighbor in self.neighbors(matriz):
            if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                probability = 100 - neighbor.density
                if self.condition == "burned":  # A intensidade do fogo é menor
                    probability -= 10
                if vent.directions:
                    if neighbor in vent.neighbors_vento(self, matriz):
                        probability = min(80, probability + 30)
                        probability = 100  # Probabilidade determinada assim para melhorar a visualização do vento
                    else:
                        probability = max(40, probability - 20)
                        probability = 0
                if (
                    random.random() < probability / 100
                ):  # queima o vizinho com probabilidade (1 - densidade da árvore)
                    neighbor.next_condition = "burning"

    def update_condition(self, forest):
        matriz = forest.matriz
        vent = forest.vent
        if self.next_condition == "burned":
            self.next_condition = "step"
            self.condition = "burned"
            self.attempt_to_burn(matriz, vent)

        elif self.next_condition == "step":
            self.step += 1
            self.attempt_to_burn(matriz, vent)
            if self.step == 3:
                self.next_condition = "final"

        elif self.next_condition == "final":
            matriz[self.x][self.y] = "v"

        if self.next_condition == "burning":  # Se o próximo estágio é queimando
            self.attempt_to_burn(
                matriz, vent
            )  # queima os vizinhos com influência do vento
            self.count += 1
            self.condition = self.next_condition
            if self.count == 2:
                self.next_condition = "burned"

    def __repr__(self):  # para visualizar a matriz
        if self.condition == "alive":
            return "1"
        if self.condition == "burning":
            return "b"
        if self.condition == "burned":
            return "0"


class Bush(Tree):
    def __init__(self, coord):

        super().__init__(coord)
        self.density = random.randint(20, 50)  # Bushes têm densidade menor que árvores


class Barrier:  # representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return "a"


class Houses(Agent):
    def __init__(self, coord, matriz):
        self.x = coord[0][0]
        self.x2 = coord[0][1]
        self.y = coord[0][0]
        self.y2 = coord[0][1]
        self.peoples = random.randint(2, 10)
        self.life = 1
        self.condition = "alive"
        self.matriz = matriz

    def __repr__(self):
        return "h"

    def neighbors(self, matriz):
        pass

    def update_condition(self):
        for neigh in self.neighbors(self.matriz):
            if neigh.condition == "burning":
                self.life -= 0.001
            if neigh.condition == "burned":
                self.life -= 0.0005
            if self.life <= 0:
                self.condition = "total_burned"

            elif self.life <= 0.5:
                self.condition = "burned"

            elif self.life <= 0.8:
                self.condition = "burning"


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
    def __init__(self, coord): 
        self.matriz=matriz
        self.aguas=[agua(i) for i in coord]