import random

class Particula:

    def __init__(self, numeroEntradas):
        self.dados = None
        self.melhorParticula = 0.0
        self.pesoTotal = 0
        self.valorTotal = 0
        self.velocidade = 0.0
        self.inicializa(numeroEntradas)

    def inicializa(self, numeroEntradas):
        self.dados = [random.randrange(0,2) for i in range(numeroEntradas)]

    def getDados(self, indice):
        return self.dados[indice]

    def getVelocidade(self):
        return self.velocidade

    def setDados(self, indice, valor):
        self.dados[indice] = valor

    def setVelocidade(self, resultadoVelocidade):
        self.velocidade = resultadoVelocidade
