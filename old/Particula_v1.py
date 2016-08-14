class Particula:
    def __init__(self,nMaxEntradas):
        self.velocidade = 0.0
        self.dados = [0] * nMaxEntradas
        self.melhorParticula = 0
       
    def get_velocidade(self):
        return self.velocidade

    def set_velocidade(self, resultadoVelocidade):
        self.velocidade = resultadoVelocidade

    def get_dados(self, indice):
        return self.dados[indice]

    def set_dados(self, indice, valor):
        self.dados[indice] = valor

    def get_melhorParticula(self):
        return self.melhorParticula

    def set_melhorParticula(self, valor):
        self.melhorParticula = valor