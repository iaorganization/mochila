from random import randint
import sys
import time
from Cromossomo import Cromossomo

def simulacaoAleatoria1():
    # Dados=  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    Pesos=  [10,22,3,49,20]
    Valores=[10,22,3,30,20]
    NmaxEntradas=5;
    NmaxParticulas=10;
    Geracoes=100;
    PesoMaximo=80;
    Maximo=0; #melhor mochila encontrada
    MelhorIndice=0;#Indice da melhor particula encontrada
    MelhorEpoca=0;#Epoca da melhor particula encontrada
    MelhorPeso=0; #
    Dados = [[0 for i in xrange(NmaxEntradas)] for i in xrange(NmaxParticulas)]
    Objetivo= 120; #peso maximo
    
    inicio_execucao = time.time()
    for h in range(Geracoes):
        for i in range(NmaxParticulas):
            Total=0;
            Peso=0;
            for j in range(NmaxEntradas):
                Dados[i][j]=randint(0,1);
                Total+=Dados[i][j]*Valores[j];
                Peso+=Dados[i][j]*Pesos[j];
            
                if j < NmaxEntradas - 1:
                    sys.stdout.write("(")
                    sys.stdout.write(str(Dados[i][j]) + " * "+ str(Valores[j]) + ") + ")
                else:
                    sys.stdout.write("(")
                    sys.stdout.write(str(Dados[i][j]) + " * "+ str(Valores[j]) + ") = ")
                        
            if Total>=Maximo and Peso<=PesoMaximo:
                Maximo=Total;
                MelhorIndice=i;
                MelhorEpoca=h;
                MelhorPeso=Peso;
            
    
    
            sys.stdout.write(str(Total)+ "\n")
        sys.stdout.write("\n Numero de epocas: " + str(h)+"\n");
    sys.stdout.write("\n Melhor resultado encontrado na epoca " + str(MelhorEpoca)+" e no indice "+ str(MelhorIndice)+ " com valor "+ str(Maximo)+" e peso "+str(MelhorPeso)+"\n");
    
    duracao = time.time() - inicio_execucao;
    print duracao

def simulacaoAleatoria2(totalSimulacoes):
    pesosLidos,valoresLidos,pesoMaximo = readConfigurationFile("mochila2.txt")
    melhorCromossomo = Cromossomo(len(pesosLidos))
    melhorCromossomo.setFitness(0)
    for i in range(0,totalSimulacoes):
        cromo = Cromossomo(len(pesosLidos))
        calculaFitness(cromo,pesosLidos,valoresLidos,pesoMaximo)
        if(cromo.getFitness() > melhorCromossomo.getFitness()):
            melhorCromossomo = cromo
        if (i % 100 == 0):
            # print "\t"+str(i)
            sys.stdout.write("\r"+str(int((100*i)/totalSimulacoes))+" %")
            sys.stdout.flush()
    print getConfiguracaoMochila(melhorCromossomo,pesosLidos,valoresLidos)
    

def calculaFitness(cromossomo,pesosLidos,valoresLidos,pesoMaximo):
    pesoTotal=0
    valorTotal=0
    for i in range(0,len(cromossomo.genes)):
        if(cromossomo.genes[i]==1):
            pesoTotal += pesosLidos[i]
            valorTotal += valoresLidos[i]
            if(pesoTotal > pesoMaximo):
                cromossomo.setFitness(0)
            else:
                cromossomo.setFitness(1.0*valorTotal-0.0*pesoTotal)

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

def getConfiguracaoMochila(cromossomo,pesosLidos,valoresLidos):
    pesoTotal = 0
    valorTotal = 0
    for i in range(0,len(cromossomo.genes)):
        if(cromossomo.genes[i]==1):
            pesoTotal += pesosLidos[i]
            valorTotal += valoresLidos[i]
    return "peso: " + str(pesoTotal)+", valor: "+ str(valorTotal) + ", fitness: " + str(cromossomo.fitness)

simulacaoAleatoria2(1000000)