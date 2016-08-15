from random import randint
import sys
import time
from Cromossomo import Cromossomo
from FileUtils import FileUtils


def simulacaoAleatoria(totalSimulacoes):
    util = FileUtils()
    pesosLidos,valoresLidos,pesoMaximo = util.readConfigurationFile("mochila2.txt")
    melhorCromossomo = Cromossomo(len(pesosLidos))
    melhorCromossomo.setFitness(0)
    for i in range(totalSimulacoes):
        cromo = Cromossomo(len(pesosLidos))
        calculaFitness(cromo,pesosLidos,valoresLidos,pesoMaximo)
        if(cromo.getFitness() > melhorCromossomo.getFitness()):
            melhorCromossomo = cromo
        print "S:-" + str(i) + getConfiguracaoMochila(melhorCromossomo,pesosLidos,valoresLidos)


def calculaFitness(cromossomo,pesosLidos,valoresLidos,pesoMaximo):
    pesoTotal=0
    valorTotal=0
    for i in range(len(cromossomo.genes)):
        if(cromossomo.genes[i]==1):
            pesoTotal += pesosLidos[i]
            valorTotal += valoresLidos[i]
            if(pesoTotal > pesoMaximo):
                cromossomo.setFitness(0)
            else:
                cromossomo.setFitness(1.0*valorTotal-0.0*pesoTotal)


def getConfiguracaoMochila(cromossomo,pesosLidos,valoresLidos):
    pesoTotal = 0
    valorTotal = 0
    for i in range(0,len(cromossomo.genes)):
        if(cromossomo.genes[i]==1):
            pesoTotal += pesosLidos[i]
            valorTotal += valoresLidos[i]
    return "-peso:-" + str(pesoTotal)+ "-valor:-"+ str(valorTotal) + "-fitness:" + str(cromossomo.fitness)

simulacaoAleatoria(1000000)