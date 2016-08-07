# -*- coding: utf-8 -*-

from FileUtils import FileUtils
from Particula2 import Particula
import math
import random
import sys
import os
import timeit

fileUtils = FileUtils()

def getValorMaximo(valores):
    soma = 0
    for i in valores:
        soma += i
    return soma

nrMaxEpocas = 5000 # Numero maximo de epocas
nrMaxParticulas = 20000 # Numero maximo de particulas
limiteInferior = 0 # Limitante minimo para a geracao de dados aleatorios
limiteSuperior = 2 # Limitante maximo para a geracao de dados aleatorios
velocidade = 10 # Velocidade maxima de mudanca de iteracoes
pesoMaximo = 35000 # Peso máximo que a mochila suporta

itensDisponiveis = fileUtils.readItensFromFile("itens.csv")
pesos = [item.peso for item in itensDisponiveis]
valores = [item.valor for item in itensDisponiveis]

nrMaxEntradas = len(valores) # Numero maximo de entradas
alvo = getValorMaximo(valores)  # Alvo que se quer atingir, isto é, soma dos valores

particulas = []

def inicializaParticula():
    for i in range(nrMaxParticulas):
        novaParticula = Particula(nrMaxEntradas)
        total = 0
        for j in range(nrMaxEntradas):
            novaParticula.setDados(j, random.randrange(limiteInferior, limiteSuperior))
            total += novaParticula.getDados(j) * pesos[j]
        novaParticula.setMelhorParticula(total)
        particulas.append(novaParticula)

def getValorParticula(indice):
    total = 0
    for i in range(nrMaxEntradas):
        total += particulas[indice].getDados(i) * valores[i]
    return total

def getPesoParticula(indice):
    peso = 0
    for i in range(nrMaxEntradas):
        peso += particulas[indice].getDados(i) * pesos[i]
    return peso

def retornaMinimo():
    # Returns an array index.
    minimo = 0
    encontraNovoMinimo = False
    feito = False

    while not feito:
        novoMinimo = False

        for i in range(nrMaxParticulas):
            if i != minimo:
                # The minimum has to be in relation to the Target.
                if math.fabs(alvo - getValorParticula(i)) < math.fabs(alvo - getValorParticula(minimo)):
                    if getPesoParticula(i) <= pesoMaximo:
                        minimo = i
                        novoMinimo = True

        if novoMinimo == False:
            feito = True
    return minimo

def atualizaVelocidade(melhorIndice):
    # From Kennedy & Eberhart(1995).
    # vx[][] = vx[][] + 2 * rand() * (pbestx[][] - presentx[][]) + 2 * rand() * (pbestx[][gbest] - presentx[][])

    resultadosTeste = 0
    melhorResultado = 0
    valor = 0.0

    melhorResultado = getValorParticula(melhorIndice)

    for i in range(nrMaxParticulas):
        resultadosTeste = getValorParticula(i)
        valor = particulas[i].getVelocidade() + 2 * random.random() * (particulas[i].getMelhorParticula() - resultadosTeste) + 2 * random.random() * (melhorResultado - resultadosTeste)

        if valor > velocidade:
            particulas[i].setVelocidade(velocidade)
        elif valor < -velocidade:
            particulas[i].setVelocidade(-velocidade)
        else:
            particulas[i].setVelocidade(valor)

def sigmoid(vid):
    y = 1/(1 + math.exp(-vid))
    return y

def successMessage(self, executionTime):
    print('Terminou com sucesso em %.2f segundos' % executionTime)

def atualizaParticulas (melhorIndice):
    for i in range(nrMaxParticulas):
        for j in range(nrMaxEntradas):
            if particulas[i].getDados(j) != particulas[melhorIndice].getDados(j):
                # Mudanca para o discreto
                if random.uniform(0, 1) < sigmoid(math.floor(particulas[i].getVelocidade())):
                    particulas[i].setDados(j, 1)
                else:
                    particulas[i].setDados(j, 0)

        # Check pBest value.
        total = getValorParticula(i)
        if math.fabs(alvo - total) < particulas[i].getMelhorParticula():
            particulas[i].setMelhorParticula(total)


def PSA():
    gMelhor = 0
    gTesteMelhor = 0
    particula1 = None
    epoca = 0
    passou = nrMaxParticulas # Particulas que passaram do limite de peso
    feito = False

    while passou == nrMaxParticulas:
        inicializaParticula()
        for i in range(nrMaxParticulas):
            if getPesoParticula(i) <= pesoMaximo:
                passou += 1;

    for i in range(nrMaxParticulas):
        if getPesoParticula(i) <= pesoMaximo:
            gMelhor = i
            break

    while not feito:
        if epoca < nrMaxEpocas:
            for i in range(nrMaxParticulas):
                if getValorParticula(i) == alvo:
                    feito = True

            gTesteMelhor = retornaMinimo()
            particula1 = particulas[gMelhor]
            if math.fabs(alvo - getValorParticula(gTesteMelhor)) < math.fabs(alvo - getValorParticula(gMelhor)):
                if getPesoParticula(gTesteMelhor) <= pesoMaximo:
                    gMelhor = gTesteMelhor

            atualizaVelocidade(gMelhor)
            atualizaParticulas(gMelhor)
            print "*****  ÉPOCA: "+ str(epoca)
            print "Peso: "+ str(getPesoParticula(gMelhor)) + ", Valor: " + str(getValorParticula(gMelhor))+"\n\n"
            epoca += 1
        else:
            feito = True
    return

def imprime():
    alvo1 = 0

    for i in range(len(particulas)):
        if getValorParticula(i) == alvo:
            alvo1 = i

    if alvo1 < len(particulas):
        print "\n"
    else:
        print "Solucao nao encontrada."
    return


if __name__ == '__main__':
    os.system("clear")
    startTime = timeit.default_timer()

    PSA()
    imprime()

    elapsed = timeit.default_timer() - startTime
    successMessage(elapsed)
