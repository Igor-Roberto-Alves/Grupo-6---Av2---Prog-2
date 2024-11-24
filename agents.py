import random


class Agente:
    # Todo agente carregará vizinhos e condiçao_de_atualizaçao
    def vizinhos(self, matriz):
        lista = []
        direçoes = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for dx, dy in direçoes:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                if isinstance(matriz[nx][ny], Arvore) or isinstance(matriz[nx][ny], Arbusto):
                    lista.append(matriz[nx][ny])

        return lista

    def condiçao_de_atualizaçao(self):
        raise NotImplementedError

    # O ideal ao criar um agente deve ser conter tudo que ele faz em condiçao_de_atualizaçao
    # Assim facilitaria atualizar o agente a cada iteração


class Animal(Agente):
    def __init__(self, matriz, x=None, y=None, ovo=False):
        self.matriz = matriz  # Matriz da floresta
        self.vida = 1
        self.status = "vivo"
        self.ovo = ovo  # A galinha está em forma de ovo ou já nasceu
        # Atributos auxiliares
        self.step = 0
        self.passo = 0
        self.morrendo = 0

        # O animal nasce em uma posição aleatória da floresta
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Arvore):
                break

        # Se for passado x,y no caso do ovo
        if x and y:
            self.x = x
            self.y = y

    def arbusto_proximo(self):
        fila = [(self.x, self.y, 0)]  # Posição atual e distância inicial
        visitados = set()
        visitados.add((self.x, self.y))

        while fila:
            cx, cy, dist = fila.pop(0)

            # Verifica se a célula atual é um arbusto
            if isinstance(self.matriz[cx][cy], Arbusto):
                return cx, cy

            # Adiciona vizinhos à fila
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= nx < len(self.matriz)
                    and 0 <= ny < len(self.matriz[0])
                    and (nx, ny) not in visitados
                    and isinstance(self.matriz[nx][ny], (Arvore, Arbusto))
                ):
                    fila.append((nx, ny, dist + 1))
                    visitados.add((nx, ny))

        return None

    def mover_para_arbusto(self):
        destino = self.arbusto_proximo()
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
                and isinstance(self.matriz[novo_x][novo_y], (Arvore, Arbusto))
            ):
                self.x = novo_x
                self.y = novo_y
        else:
            self.andar()

    def atualizar_vida(self):
        # Se a galinha nao está em um arbusto ela está passando fome
        faminto = True
        lista_vizinhos = self.vizinhos(self.matriz)
        lista_vizinhos.append(self.matriz[self.x][self.y])
        for vizinho in lista_vizinhos:
            if isinstance(vizinho, Arbusto):
                faminto = False  # Não está com fome se estiver em um arbusto
            if isinstance(vizinho, Arvore) or isinstance(
                vizinho, Arbusto
            ):  # Se algum vizinho contando seu próprio lugar, estiver pegando fogo
                if vizinho.condiçao == "queimando":
                    self.vida -= 0.1
                    if self.ovo:  # Se for um ovo morre instantaneamente
                        self.vida -= 1
        if faminto:  # A cada passo com fome perde 0.1 de vida
            self.vida -= 0.1

        if self.vida <= 0:
            self.status = "morto"
            if self.ovo:
                self.status = "final"

    def condiçao_de_atualizaçao(self):
        if not self.ovo and self.status != "morto" and self.status != "final":
            self.passo += 1
            if self.passo == 4:
                self.mover_para_arbusto()
                self.atualizar_vida()
                self.passo = 0
            return self.procriar()
        if self.status == "morto":
            self.morrendo += 1
            if self.morrendo == 100:

                self.status = "final"

        elif self.ovo:
            self.step += 1
            self.atualizar_vida()
            if self.step == 20:
                self.ovo = False
                self.vida = 1
        return None

    def andar(self):

        direçoes = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        ]
        random.shuffle(direçoes)
        direçoes_possiveis = []
        for dx, dy in direçoes:
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= nx < len(self.matriz)
                and 0 <= ny < len(self.matriz[0])
                and (
                    isinstance(self.matriz[nx][ny], Arvore) or self.matriz[nx][ny] == "grama"
                )
            ):
                self.x, self.y = nx, ny  # Move o bombeiro para a nova posição
                direçoes_possiveis.append((nx, ny))

        if direçoes_possiveis:
            a = random.choice(direçoes_possiveis)
            self.x, self.y = a[0], a[1]

    def procriar(self):
        if self.status == "vivo":
            a = random.randint(1, 200)  # Põem um ovo com esta probabilidade
            if a == 1:
                return Animal(self.matriz, self.x, self.y, True)


"""""
class Passaro:
    def __init__(self, matriz, x=None, y=None):
        self.matriz = matriz
        self.condiçao = "vivo"
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Arvore):
                break

        if x and y:
            self.x = x
            self.y = y
        self.spread_prob = 1  # Chance de semear uma árvore.
        self.step = 0

    def condiçao_de_atualizaçao(self):
        self.step += 1
        if self.step == 3:
            dx, dy = random.randint(-2, 2), random.randint(-2, 2)
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(self.matriz) and 0 <= ny < len(self.matriz[0]):
                self.x, self.y = nx, ny
                if self.matriz[nx][ny] == "grama" and random.random() < self.spread_prob:
                    b = random.randint(1, 3)
                    if b == 1:
                        self.matriz[nx][ny] = Arvore([nx, ny])
                    else:
                        self.matriz[nx][ny] = Arbusto([nx, ny])
                elif self.matriz[nx][ny] == "preto":
                    self.condiçao = "remove"
            else:
                self.condiçao = "remove"
            self.step = 0

    def atualizar_populacao_de_passaros(self, lista_de_passaros):
        for passaro in lista_de_passaros:
            if passaro.condiçao == "remove":
                lista_de_passaros.remove(passaro)

        a = random.randint(0, 10)
        if a == 1:
            lista_de_passaros.append(Bird(self.matriz))
""" ""


class Passaro:
    def __init__(self, matriz, x=None, y=None):
        if x and y:
            self.x, self.y = x, y
        else:
            while True:
                self.x = random.randint(0, len(matriz) - 1)
                self.y = random.randint(0, len(matriz[0]) - 1)
                celula = matriz[self.x][self.y]
                if isinstance(celula, Arvore):
                    break

        self.status = "vivo"
        self.idade = 0
        self.espectativa_vida = random.randint(20, 50)
        self.matriz = matriz

    def movimento(self):
        if self.status != "vivo":
            return

        direçao = random.choice(["cima", "baixo", "esquerda", "direita"])
        if direçao == "cima":
            self.x -= 1
        elif direçao == "baixo":
            self.x += 1
        elif direçao == "esquerda":
            self.y -= 1
        elif direçao == "direita":
            self.y += 1

        if self.x < 0 or self.x >= len(self.matriz):
            self.status = "morto"
        elif self.y < 0 or self.y >= len(self.matriz[0]):
            self.status = "morto"
        elif self.matriz[self.x][self.y] == "preto":
            self.status = "morto"

    def plantar_arvore(self, prob_semente=0.1, prob_arbusto=0.1):
        if self.status != "vivo":
            return

        if self.matriz[self.x][self.y] == "grama" and random.random() < prob_semente:
            self.matriz[self.x][self.y] = Arvore([self.x, self.y])
        elif self.matriz[self.x][self.y] == "grama" and random.random() < prob_arbusto:
            self.matriz[self.x][self.y] = Arbusto([self.x, self.y])

    def checar_fogo(self, raio_fogo=1):
        if self.status != "vivo":
            return False

        for dx in range(-raio_fogo, raio_fogo + 1):
            for dy in range(-raio_fogo, raio_fogo + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(self.matriz) and 0 <= ny < len(self.matriz[0]):
                    celula = self.matriz[nx][ny]
                    if isinstance(celula, Arvore) and celula.condiçao == "queimando":
                        self.status = "queimando"
                        return True
        return False

    def reproduzir(self, passaros, prob_acasalar=0.1, max_passaros=300):
        if len(passaros) >= max_passaros:
            return
        if (
            self.idade >= 10
        ):  # O pássaro pode começar a se reproduzir após atingir certa idade
            # Verificar se há outros pássaros nas proximidades
            passaros_perto = [
                passaro
                for passaro in passaros
                if abs(passaro.x - self.x) <= 3
                and abs(passaro.y - self.y) <= 3
                and passaro != self
            ]
            if (
                passaros_perto and random.random() < prob_acasalar
            ):  # 10% de chance de reprodução
                # Gerar um novo pássaro em uma posição próxima
                novo_passaro = Passaro(
                    self.matriz,
                    x=self.x + random.choice([-1, 0, 1]),
                    y=self.y + random.choice([-1, 0, 1]),
                )
                passaros.append(novo_passaro)

    def condiçao_de_atualizaçao(self, passaros):
        if self.status == "morto":
            return

        self.movimento()
        self.plantar_arvore()
        self.reproduzir(passaros)
        self.idade += 1

        if self.idade >= self.espectativa_vida:
            self.status = "morto"

    def atualizar_populacao_de_passaros(self, lista_de_passaros):
        lista_de_passaros[:] = [passaro for passaro in lista_de_passaros if passaro.status != "morto"]


class Arvore(Agente):
    def __init__(self, coord):
        self.condiçao = "vivo"
        self.umidade = random.randint(75, 80)  # Resistência ao fogo baseada na umidade
        self.proxima_condiçao = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0  # Contador para etapas de queima
        self.step = 0  # Etapas que a árvore passa antes de ser "final"

    def propagar_fogo(self, matriz, vent):
        """
        Tenta propagar o fogo para os vizinhos com base na condição atual,
        umidade e influência do vento.
        """
        for vizinho in self.vizinhos(matriz):
            if vizinho.condiçao == "vivo" and vizinho.proxima_condiçao != "queimando":
                # Calcula a probabilidade base de queima
                probabilidade_base = 100 - vizinho.umidade

                # Reduz a probabilidade se o fogo estiver se dissipando
                if self.condiçao == "queimado":
                    probabilidade_base -= 10  # Fogo menos intenso

                # Ajusta com base no vento
                if vent.direçoes:
                    if vizinho in vent.vizinhos_vento(self, matriz):
                        probabilidade_base = min(
                            90, probabilidade_base + 15
                        )  # Aumenta devido ao vento
                    else:
                        probabilidade_base = random.randint(3, 7)
                        # Reduz se fora da direção do vento
                # Probabilidade ajustada com um fator de suavização
                probabilidade = max(
                    0, min(100, probabilidade_base)
                )  # Garante limite entre 0 e 100

                # Tenta queimar o vizinho
                if random.random() < probabilidade / 100:
                    vizinho.proxima_condiçao = "queimando"

    def condiçao_de_atualizaçao(self, floresta):
        """
        Atualiza a condição da árvore com base no estado atual e propaga o fogo para os vizinhos.
        """
        matriz = floresta.matriz
        vent = floresta.vent

        if self.proxima_condiçao == "queimado":
            self.condiçao = "queimado"
            self.step += 1  # Passa um passo como "queimada"
            if self.step == 3:  # Após 3 etapas, marca como finalizada
                self.proxima_condiçao = "final"
            else:
                self.propagar_fogo(matriz, vent)

        elif self.proxima_condiçao == "final":
            matriz[self.x][self.y] = "grama"  # Some

        elif self.proxima_condiçao == "queimando":
            self.count += 1  # Incrementa o contador enquanto está queimando
            self.condiçao = self.proxima_condiçao
            if self.count == 2:
                self.propagar_fogo(matriz, vent)  # Propaga o fogo para os vizinhos
            if self.count > 2:  # Queima por 2 etapas antes de ser marcada como "queimado"
                self.proxima_condiçao = "queimado"

    def __repr__(self):
        """
        Representação textual da árvore na matriz:
        - '1' para viva
        - 'b' para queimando
        - '0' para queimada
        """
        if self.condiçao == "vivo":
            return "1"
        if self.condiçao == "queimando":
            return "b"
        if self.condiçao == "queimado":
            return "0"


class Arbusto(Arvore):
    def __init__(self, coord):

        super().__init__(coord)
        self.umidade = random.randint(50, 60)  # Arbustos têm umidade menor que árvores


class bombeiro(Agente):
    def __init__(self, matriz, x=None, y=None):
        self.step = 0  # Definindo o numero de atualizações para o bombeiro andar
        self.matriz = matriz  # Matriz da floresta
        self.vida = 1  # O bombeiro terá vida igual a 1 e perderá conforme as árvores ao seu redor pegam fogo
        self.status = "vivo"

        # Posição aleatória em que o bombeiro nascerá
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Arvore):
                break
        if x and y:
            self.x, self.y = x, y

    def condiçao_de_atualizaçao(self):
        self.andar()  # O bomebiro anda
        # Verificando árvores que estão queimando
        self.apaga_fogo()
        for vizinho in self.vizinhos(self.matriz):
            if isinstance(vizinho, Arvore):
                if vizinho.condiçao == "queimando":
                    self.vida -= 0.01

        if 0.5 <= self.vida <= 0.8:
            self.status = "queimando"

        elif 0 < self.vida < 0.5:
            self.status = "queimando"

        elif self.vida <= 0:
            self.status = "morto"

    def andar(self):
        # A função andar, por enquanto apenas leva o bombeiro para um vizinho aleatório
        self.step += 1
        if self.step == 5:
            direçoes = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
            ]
            random.shuffle(direçoes)
            direçoes_possiveis = []
            for dx, dy in direçoes:
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < len(self.matriz)
                    and 0 <= ny < len(self.matriz[0])
                    and (
                        isinstance(self.matriz[nx][ny], Arvore)
                        or self.matriz[nx][ny] == "grama"
                    )
                ):
                    self.x, self.y = nx, ny  # Move o bombeiro para a nova posição
                    direçoes_possiveis.append((nx, ny))

            if direçoes_possiveis:
                a = random.choice(direçoes_possiveis)
                self.x, self.y = a[0], a[1]

            self.step = 0

    def apaga_fogo(self):
        # Obtém os vizinhos ao redor do bombeiro
        vizinhos = self.vizinhos(self.matriz)

        # Verifica a posição atual do bombeiro e adiciona à lista de vizinhos, se necessário
        if self.matriz[self.x][self.y] != "grama":
            vizinhos.append(self.matriz[self.x][self.y])

        # Itera sobre os vizinhos
        for vizinho in vizinhos:
            if isinstance(vizinho, Arvore):
                # Verifica se a árvore está no estágio "queimando"
                if (
                    vizinho.condiçao == "queimando"
                ):
                    # Apaga o fogo da árvore, criando uma nova árvore no estado saudável
                    self.matriz[vizinho.x][vizinho.y] = Arvore([vizinho.x, vizinho.y])
                    break  # Apaga o fogo de apenas uma árvore de cada vez
            elif isinstance(vizinho, Arbusto):
                # Verifica se o arbusto está no estágio "queimando"
                if (
                    vizinho.condiçao == "queimando"
                ):
                    # Apaga o fogo do arbusto, criando um novo arbusto no estado saudável
                    self.matriz[vizinho.x][vizinho.y] = Arbusto([vizinho.x, vizinho.y])
                    break  # Apaga o fogo de apenas um arbusto de cada vez


class Botao:
    def __init__(self, x, y, largura, altura):
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.visivel = True

    def esta_clicado(self, pos):
        if self.visivel:
            return (
                self.x <= pos[0] <= self.x + self.largura
                and self.y <= pos[1] <= self.y + self.altura
            )
        else:
            return None


class Barreira:  # representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return "a"


# Classe auxiliadora que representa
class H(Agente):
    def __init__(self, coord):
        self.x, self.y = coord

    def __repr__(self):
        return "H"


class Casa(Agente):
    def __init__(self, coord):

        self.condiçao = "seguro"
        self.init = True
        self.coord = coord
    def coords(self, matriz):
        """
        Define as coordenadas de um quadrado 3x3 ao redor do ponto central (x, y),
        ajustando o quadrado caso as coordenadas originais não sejam válidas.

        Retorna as coordenadas válidas ou None se não for possível encontrar um bloco 3x3 válido.
        """
        x, y = self.coord[0], self.coord[1]  # Coordenada inicial
        direçoes = [
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

        for dx, dy in direçoes:
            # Ajustar a posição central com base na direção
            nx, ny = x + dx, y + dy
            coords = [(nx + dx, ny + dy) for dx in range(-1, 2) for dy in range(-1, 2)]

            # Verificar se o bloco 3x3 na posição ajustada é válido
            valido = True
            for cx, cy in coords:
                if not (0 <= cx < len(matriz) and 0 <= cy < len(matriz[0])):
                    valido = False
                    break
                if matriz[cx][cy] == "preto":
                    valido = False
                    break

            # Retorna as coordenadas válidas assim que encontrar
            if valido:
                return coords

        # Se nenhuma posição for válida, retorna None
        return None

    def checar_vizinhos(self, matriz):
        coordenadas_casa = self.coords()
        for coord in coordenadas_casa:
            coord.vizinhos(matriz)
            for nx, ny in self.vizinhos:
                if 0 <= nx < len(self.matriz) and 0 <= ny < len(self.matriz[0]):
                    vizinho = self.matriz[nx][ny]
                    if (
                        isinstance(vizinho, (Arvore, Arbusto))
                        and vizinho.condiçao == "queimando"
                    ):
                        self.vida -= 0.01
                        return

    def checar_vida(self):
        if self.vida <= 0:
            self.condiçao = "fim"

    def condiçao_de_atualizaçao(self):
        self.checar_vizinhos()
        self.checar_vida()


class vento:
    def __init__(self, direçao=None):
        lista_direçoes = ["N", "S", "L", "O", "NO", "NE", "SE", "SO"]
        self.direçoes = []
        if direçao == 1:
            direçao = random.choice(lista_direçoes)
        if direçao == "L":
            self.direçoes = [(0, 1), (1, 1), (-1, 1)]
        elif direçao == "O":
            self.direçoes = [(0, -1), (1, -1), (-1, -1)]
        elif direçao == "S":
            self.direçoes = [(1, 0), (1, 1), (1, -1)]
        elif direçao == "N":
            self.direçoes = [(-1, 0), (-1, 1), (-1, -1)]
        elif direçao == "SE":
            self.direçoes = [(0, 1), (1, 0), (1, 1)]
        elif direçao == "NE":
            self.direçoes = [(0, 1), (-1, 0), (-1, 1)]
        elif direçao == "SO":
            self.direçoes = [(0, -1), (1, 0), (1, -1)]
        elif direçao == "NO":
            self.direçoes = [(0, -1), (-1, 0), (-1, -1)]

    def vizinhos_vento(self, arvore, matriz):
        lista = []
        if self.direçoes:
            for dx, dy in self.direçoes:
                nx, ny = arvore.x + dx, arvore.y + dy
                if (
                    0 <= nx < len(matriz)
                    and 0 <= ny < len(matriz[0])
                    and isinstance(matriz[nx][ny], Arvore)
                ):
                    lista.append(matriz[nx][ny])

        return lista
