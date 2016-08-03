from Particula import Particula
import random
import math
import sys
import time


def getValorMaximo(valores):
    soma=0
    for i in valores:
        soma+=i
    print "Valor maximo: " + str(soma) 
    return soma

def readConfigurationFile(fileName):
    file = open(fileName,"r")
    dados=[]
    for line in file:
        dados.append(line)

    pesos = dados[0]
    pesos = pesos.split(",")
    pesos = map(int,pesos)
    valores = dados[1]
    valores = valores.split(",")
    valores = map(int,valores)
    pesoMaximo = dados[2]
    pesoMaximo = int(pesoMaximo)
    return pesos,valores,pesoMaximo


nMaxParticulas = 20000 #Numero maximo de particulas
velocidade = 10 #velocidade maxima de mudanca de iteracoes
# PesoMaximo = 50;

nMaxEpocas = 5000; #Numero maximo de epocas

LimiteInferior = 0 #Limitante minimo para a geracao de dados aleatorios
LimiteSuperior = 2# Limitante maximo para a geracao de dados aleatorios

Pesos,Valores,PesoMaximo = readConfigurationFile("mochila2.txt")
# Valores=[2,3,4,5,6,7,8,9,10,11]
# Pesos=  [1,2,3,4,5,6,7,8,9,10]
NmaxEntradas = len(Valores) #Numero maximo de entradas
Alvo= getValorMaximo(Valores)  #Alvo que se quer atingir: soma dos valores

Particulas = []





def inicializa_particula():
    for i in range(nMaxParticulas):
        NovaParticula = Particula(NmaxEntradas)
        Total = 0
        for j in range(NmaxEntradas):
            NovaParticula.set_dados(j, random.randrange(LimiteInferior, LimiteSuperior))
            Total += NovaParticula.get_dados(j)* Pesos[j];
        
        NovaParticula.set_melhorParticula(Total)
        Particulas.append(NovaParticula)


def getValorParticula(Indice):
    Total = 0
    for i in range(NmaxEntradas):
        Total += Particulas[Indice].get_dados(i)*Valores[i]
    return Total


def getPesoParticula(Indice):
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
        
        for i in range(nMaxParticulas):
            if i != Minimo:
                # The minimum has to be in relation to the Target.
                if math.fabs(Alvo - getValorParticula(i)) < math.fabs(Alvo - getValorParticula(Minimo)):
                    if getPesoParticula(i) <= PesoMaximo:
                        Minimo = i
                        NovoMinimo = True
        
        if NovoMinimo == False:
            Feito = True
    
    return Minimo
    
    
def atualizaVelocidade(MelhorIndice):
    # from Kennedy & Eberhart(1995).
    #   vx[][] = vx[][] + 2 * rand() * (pbestx[][] - presentx[][]) + 2 * rand() * (pbestx[][gbest] - presentx[][])
    
    ResultadosTeste = 0
    MelhorResultado = 0
    Valor = 0.0
    
    MelhorResultado = getValorParticula(MelhorIndice)
    
    for i in range(nMaxParticulas):
        ResultadosTeste = getValorParticula(i)
        Valor = Particulas[i].get_velocidade() + 2 * random.random() * (Particulas[i].get_melhorParticula() - ResultadosTeste) + 2 * random.random() * (MelhorResultado - ResultadosTeste)
        
        if Valor > velocidade:
            Particulas[i].set_velocidade(velocidade)
        elif Valor< - velocidade:
            Particulas[i].set_velocidade(-velocidade)
        else:
            Particulas[i].set_velocidade(Valor)
    

def sigmoid(vid):
    y=1/(1+ math.exp(-vid))
    return y


def atualizaParticulas (MelhorIndice):
    for i in range(nMaxParticulas):
        for j in range(NmaxEntradas):
            if Particulas[i].get_dados(j) != Particulas[MelhorIndice].get_dados(j):
                # Mudanca para o discreto
                if random.uniform(0, 1) < sigmoid(math.floor(Particulas[i].get_velocidade())) :
                    Particulas[i].set_dados(j, 1)
                else:
                    Particulas[i].set_dados(j, 0)
                
        # Check pBest value.
        Total = getValorParticula(i)
        if math.fabs(Alvo - Total) < Particulas[i].get_melhorParticula():
            Particulas[i].set_melhorParticula(Total)


def PSA():
    GMelhor = 0
    GTesteMelhor = 0
    Particula1 = None
    Epoca = 0
    Passou= nMaxParticulas #Particulas que passaram do limite de peso
    Feito = False

    while Passou==nMaxParticulas:
        inicializa_particula()
        for i in range(nMaxParticulas):
            if getPesoParticula(i)<=PesoMaximo:
                Passou+=1;

    for i in range(nMaxParticulas):
        if getPesoParticula(i)<=PesoMaximo:
            GMelhor=i;
            break;

    while not Feito:
        print " epoca: "+ str(Epoca)
        if Epoca < nMaxEpocas:
            for i in range(nMaxParticulas):
                if getValorParticula(i) == Alvo:
                    Feito = True
            
            GTesteMelhor = retorna_minimo()
            Particula1 = Particulas[GMelhor]
            if math.fabs(Alvo - getValorParticula(GTesteMelhor)) < math.fabs(Alvo - getValorParticula(GMelhor)):
                if getPesoParticula(GTesteMelhor) <= PesoMaximo:
                    GMelhor = GTesteMelhor
            
            
            atualizaVelocidade(GMelhor)
            atualizaParticulas(GMelhor)
            
            sys.stdout.write("\n Numero de epocas: " + str(Epoca));
            sys.stdout.write("\n Peso: "+ str(getPesoParticula(GMelhor)) + ", Valor: " + str(getValorParticula(GMelhor))+"\n");
            
            Epoca += 1
        else:
            Feito = True
    return

# Imprime o resultado na tela
def imprime():
    Alvo1 = 0
    
    for i in range(len(Particulas)):
        if getValorParticula(i) == Alvo:
            Alvo1 = i
    
    if Alvo1 < len(Particulas):
        sys.stdout.write("\n")
    else:
        sys.stdout.write("\nSolucao nao encontrada.")
    return


if __name__ == '__main__':
    tempo=0;
    for i in range(1):
        inicio_execucao = time.time()    
        PSA()
        imprime()
        duracao = time.time() - inicio_execucao
        sys.stdout.write("Tempo total da execucao: " + str(duracao) + " segundos\n" )
        
        tempo+=duracao;
    tempo=tempo/5;
    sys.stdout.write("Media: " + str(tempo) + " segundos \n" )
    