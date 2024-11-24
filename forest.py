import agents as ag
import random


class Floresta:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = ag.vento()
        self.surgir_arvores = False

    def incendio(self):
        k = random.randint(0, self.n - 1)
        l = random.randint(0, self.m - 1)
        if (
            isinstance(self.matriz[k][l], ag.Arvore)
            and self.matriz[k][l].condiçao == "vivo"
        ):
            self.matriz[k][l].propagar_fogo(self.matriz, self.vent)
                

    def atualizar_floresta(self):
        fogo = True
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.matriz[i][j], ag.Arvore) or isinstance(
                    self.matriz[i][j], ag.Arbusto
                ):
                    if (
                        self.matriz[i][j].condiçao == "queimando"
                        or self.matriz[i][j].condiçao == "queimado"
                    ):
                        fogo = False

                    self.matriz[i][j].condiçao_de_atualizaçao(self)

                if self.surgir_arvores:
                    rand = random.randint(1, 200)
                    if rand > 195:
                        if self.matriz[i][j] == "grama":
                            self.matriz[i][j] = ag.Arvore([i, j])
                    if rand == 1:
                        if self.matriz[i][j] == "grama":
                            self.matriz[i][j] = ag.Arbusto([i, j])
        if fogo:
            self.incendio()  # Caso não tenha fogo, causa um incêndio aleatório
