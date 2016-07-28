import random
import math
import sys
import time

Alvo= 210  #Alvo que se quer atingir
NmaxEntradas = 6 #Numero maximo de entradas
NmaxParticulas = 10 #Numero maximo de particulas
Velocidade = 10 #Velocidade maxima de mudanca de iteracoes
PesoMaximo = 7;

NmaxEpocas = 10; #Numero maximo de epocas

LimiteInferior = 0 #Limitante minimo para a geracao de dados aleatorios
LimiteSuperior = 2# Limitante maximo para a geracao de dados aleatorios


Valores=[10,20,30,40,50,60]
Pesos=[1,2,3,4,5,6]


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
            Total += NovaParticula.get_dados(j)* Pesos[j];
        
        NovaParticula.set_melhorParticula(Total)
        Particulas.append(NovaParticula)
    return

def testa_dados(Indice):
    Total = 0
    for i in range(NmaxEntradas):
        Total += Particulas[Indice].get_dados(i)*Valores[i]
            #if testa_peso(Indice) > PesoMaximo:
            #Total= PesoMaximo-testa_peso(Indice);
            

    return Total

def testa_peso(Indice):
    Peso = 0
    
    for i in range(NmaxEntradas):
        Peso += Particulas[Indice].get_dados(i)*Pesos[i]
    
    return Peso
    
    
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
                    if testa_peso(i) <= PesoMaximo:
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
    Passou= NmaxParticulas #Particulas que passaram do limite de peso
    Feito = False


    while Passou==NmaxParticulas:
        inicializa_particula()
        for i in range(NmaxParticulas):
            if testa_peso(i)<=PesoMaximo:
                Passou+=1;


    for i in range(NmaxParticulas):
        if testa_peso(i)<=PesoMaximo:
            GMelhor=i;
            break;

    while not Feito:
        # Two conditions can end this loop:
        # if the maximum number of epochs allowed has been reached, or,
        # if the Target value has been found.
        if Epoca < NmaxEpocas:
            for i in range(NmaxParticulas):
                for j in range(NmaxEntradas):
                    if j < NmaxEntradas - 1:
                        sys.stdout.write("(") 
                        sys.stdout.write(str(Particulas[i].get_dados(j)) + " * "+ str(Valores[j]) + ") + ")
                    else:
                        sys.stdout.write("(") 
                        sys.stdout.write(str(Particulas[i].get_dados(j)) + " * "+ str(Valores[j]) + ") = ")
                     

                #sys.stdout.write(str(bin(testa_dados(i)))+ "\n")
                sys.stdout.write(str(testa_dados(i))+ "\n")
                if testa_dados(i) == Alvo:
                    Feito = True
            
            GTesteMelhor = retorna_minimo()
            Particula1 = Particulas[GMelhor]
            if math.fabs(Alvo - testa_dados(GTesteMelhor)) < math.fabs(Alvo - testa_dados(GMelhor)):
                if testa_peso(GTesteMelhor) <= PesoMaximo:
                    GMelhor = GTesteMelhor
            
                        
            
            
            retorna_velocidade(GMelhor)
            
            atualiza_particulas(GMelhor)
            
            sys.stdout.write("\n Numero de epocas: " + str(Epoca));
            sys.stdout.write("\n")
            sys.stdout.write("Melhor: " + str(GMelhor))
            sys.stdout.write("\n Peso maximo dessa geracao: "+ str(testa_peso(GMelhor)) + "\n");
            
            
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
        for i in range(NmaxEntradas):
            if i < NmaxEntradas - 1:
                sys.stdout.write("(") 
                sys.stdout.write(str(Particulas[Alvo1].get_dados(i)) + " * "+ str(Valores[i]) + ") + ")
            else:
                sys.stdout.write("(") 
                sys.stdout.write(str(Particulas[Alvo1].get_dados(i)) + " * "+ str(Valores[i]) + ") eh o mais proximo de satisfazer o prblema")
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
    sys.stdout.write("Media: " + str(tempo) + " segundos \n" )
    