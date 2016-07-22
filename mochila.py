import random
import math
import sys
import time

Alvo= 30  #Alvo que se quer atingir
NmaxEntradas = 6 #Numero maximo de entradas
NmaxParticulas = 3 #Numero maximo de particulas
Velocidade = 10 #Velocidade maxima de mudanca de iteracoes

NmaxEpocas = 10; #Numero maximo de epocas

LimiteInferior = 0 #Limitante minimo para a geracao de dados aleatorios
LimiteSuperior = 2# Limitante maximo para a geracao de dados aleatorios


Pesos=[4,6,8,7,9,10]


Particulas = []

class Particula:
    def __init__(self):
        self.velocidade = 0.0
        self.dados = [0] * NmaxEpocas
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

  

def inicializa_particula():
    for i in range(NmaxParticulas):
        NovaParticula = Particula()
        Total = 0
        for j in range(NmaxEntradas):
            NovaParticula.set_dados(j, random.randrange(LimiteInferior, LimiteSuperior))
            Total += NovaParticula.get_dados(j)* Pesos[i];

        NovaParticula.set_melhorParticula(Total)
        Particulas.append(NovaParticula)
    return

def testa_dados(Indice):
    Total = 0

    for i in range(NmaxEntradas):
        Total += Particulas[Indice].get_dados(i)*Pesos[i]

    return Total
    
    
def retorna_minimo():
    # Returns an array index.
    Minimo = 0
    encontraNovoMinimo = False
    Feito = False
    
    while not Feito:
        NovoMinimo = False
        
        for i in range(NmaxParticulas):
            if i != Minimo:
                # The minimum has to be in relation to the Target.
                if math.fabs(Alvo - testa_dados(i)) < math.fabs(Alvo - testa_dados(Minimo)):
                    Minimo = i
                    NovoMinimo = True
        
        if NovoMinimo == False:
            Feito = True
    
    return Minimo
    
    
def retorna_velocidade(MelhorIndice):
    # from Kennedy & Eberhart(1995).
    #   vx[][] = vx[][] + 2 * rand() * (pbestx[][] - presentx[][]) + 2 * rand() * (pbestx[][gbest] - presentx[][])
    
    ResultadosTeste = 0
    MelhorResultado = 0
    Valor = 0.0
    
    MelhorResultado = testa_dados(MelhorIndice)
    
    for i in range(NmaxParticulas):
        ResultadosTeste = testa_dados(i)
        Valor = Particulas[i].get_velocidade() + 2 * random.random() * (Particulas[i].get_melhorParticula() - ResultadosTeste) + 2 * random.random() * (MelhorResultado - ResultadosTeste)
        
        if Valor > Velocidade:
            Particulas[i].set_velocidade(Velocidade)
        elif Valor< - Velocidade:
            Particulas[i].set_velocidade(-Velocidade)
        else:
            Particulas[i].set_velocidade(Valor)
    
    return

def sigmoid(vid):
    y=1/(1+ math.exp(-vid))
    return y


def atualiza_particulas (MelhorIndice):
    for i in range(NmaxParticulas):
        for j in range(NmaxEntradas):
            if Particulas[i].get_dados(j) != Particulas[MelhorIndice].get_dados(j):
                # Mudanca para o discreto
                if random.uniform(0, 1) < sigmoid(math.floor(Particulas[i].get_velocidade())) :
                    Particulas[i].set_dados(j, 1)
                else:
                    Particulas[i].set_dados(j, 0)
                
                
        
        # Check pBest value.
        Total = testa_dados(i)
        if math.fabs(Alvo - Total) < Particulas[i].get_melhorParticula():
            Particulas[i].set_melhorParticula(Total)
    
    return


def PSA():
    GMelhor = 0
    GTesteMelhor = 0
    Particula1 = None
    Epoca = 0
    Feito = False

    inicializa_particula()

    while not Feito:
        # Two conditions can end this loop:
        # if the maximum number of epochs allowed has been reached, or,
        # if the Target value has been found.
        if Epoca < NmaxEpocas:
            for i in range(NmaxParticulas):
                for j in range(NmaxEntradas):
                    if j < NmaxEntradas - 1:
                        sys.stdout.write("(") 
                        sys.stdout.write(str(Particulas[i].get_dados(j)) + " * "+ str(Pesos[j]) + ") + ")
                    else:
                        sys.stdout.write("(") 
                        sys.stdout.write(str(Particulas[i].get_dados(j)) + " * "+ str(Pesos[j]) + ") = ")
                     

                #sys.stdout.write(str(bin(testa_dados(i)))+ "\n")
                sys.stdout.write(str(testa_dados(i))+ "\n")
                if testa_dados(i) == Alvo:
                    Feito = True
            
            GTesteMelhor = retorna_minimo()
            Particula1 = Particulas[GMelhor]
            if math.fabs(Alvo - testa_dados(GTesteMelhor)) < math.fabs(Alvo - testa_dados(GMelhor)):
                GMelhor = GTesteMelhor
            
            retorna_velocidade(GMelhor)
            
            atualiza_particulas(GMelhor)
            
            sys.stdout.write("\nNumero de epocas: " + str(Epoca))
            sys.stdout.write("\n")
            
            Epoca += 1
        else:
            Feito = True
    
    return

# Imprime o resultado na tela
def imprime():
    # Find solution particle.
    Alvo1 = 0
    
    for i in range(len(Particulas)):
        if testa_dados(i) == Alvo:
            Alvo1 = i
    
    # Print it.
    if Alvo1 < len(Particulas):
        sys.stdout.write("\nParticula " + str(Alvo1) + " acertou o alvo.\n")
        for i in range(NmaxEntradas):
            if i < NmaxEntradas - 1:
                sys.stdout.write("(") 
                sys.stdout.write(str(Particulas[Alvo1].get_dados(i)) + " * "+ str(Pesos[i]) + ") + ")
            else:
                sys.stdout.write("(") 
                sys.stdout.write(str(Particulas[Alvo1].get_dados(i)) + " * "+ str(Pesos[i]) + ") eh o mais proximo do alvo: " + str(Alvo))
             #if i >= NmaxEntradas - 1:
                #sys.stdout.write(str(bin(Alvo)))
        
        sys.stdout.write("\n")
    else:
        sys.stdout.write("\nSolucaoo nao encontrada.")
        
    

    
    return


if __name__ == '__main__':
    tempo=0;
    for i in range(5):
        inicio_execucao = time.time()    
        PSA()
        imprime()
        duracao = time.time() - inicio_execucao
        sys.stdout.write("Tempo total da execucao: " + str(duracao) + " segundos\n" )
        
        tempo+=duracao;
    tempo=tempo/5;
    sys.stdout.write("Media: " + str(tempo) + " segundos" )
    