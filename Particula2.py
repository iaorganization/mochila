class Particula:
    def __init__(self, nrMaxEntradas):
        self.velocidade = 0.0
        self.dados = [0] * nrMaxEntradas
        self.melhorParticula = 0

    def getVelocidade(self):
        return self.velocidade

    def setVelocidade(self, resultadoVelocidade):
        self.velocidade = resultadoVelocidade

    def getDados(self, indice):
        return self.dados[indice]

    def setDados(self, indice, valor):
        self.dados[indice] = valor

    def getMelhorParticula(self):
        return self.melhorParticula

    def setMelhorParticula(self, valor):
        self.melhorParticula = valor