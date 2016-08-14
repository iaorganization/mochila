# -*- coding: utf-8 -*-

from FileUtils import FileUtils
from Particula import Particula
import math
import random
import sys
import os
import timeit

util = FileUtils()

numeroEpocas = 5000 # Numero maximo de epocas
numeroParticulas = 20000 # Numero maximo de particulas
velocidade = 10 # Velocidade maxima de mudanca de iteracoes

pesos, valores, pesoMaximo = util.readConfigurationFile("mochila2.txt")

numeroEntradas = len(valores) # Numero maximo de entradas
alvo = sum(valores)  # Alvo que se quer atingir, isto é, a soma dos valores

particulas = []

def atualizaParticulas(melhorIndice):
    for i in range(numeroParticulas):
        for j in range(numeroEntradas):
            if particulas[i].getDados(j) != particulas[melhorIndice].getDados(j):
                if random.uniform(0, 1) < sigmoid(math.floor(particulas[i].getVelocidade())):
                    particulas[i].setDados(j, 1)
                else:
                    particulas[i].setDados(j, 0)

        atualizaPesoTotalParticula(i)
        atualizaValorTotalParticula(i)

        if math.fabs(alvo - particulas[i].valorTotal) < particulas[i].melhorParticula:
            particulas[i].melhorParticula = particulas[i].valorTotal

def atualizaPesoTotalParticula(indice):
    pesoTotal = sum([i*j for i,j in zip(particulas[indice].dados, pesos)])
    particulas[indice].pesoTotal = pesoTotal
    return pesoTotal

def atualizaValorTotalParticula(indice):
    valorTotal = sum([i*j for i,j in zip(particulas[indice].dados, valores)])
    particulas[indice].valorTotal = valorTotal
    return valorTotal

def atualizaVelocidade(melhorIndice):
    resultadosTeste = 0
    melhorResultado = 0
    valor = 0.0

    melhorResultado = particulas[melhorIndice].valorTotal

    for i in range(numeroParticulas):
        resultadosTeste = particulas[i].valorTotal
        valor = particulas[i].getVelocidade() + 2 * random.random() * (particulas[i].melhorParticula - resultadosTeste) + 2 * random.random() * (melhorResultado - resultadosTeste)

        if valor > velocidade:
            particulas[i].setVelocidade(velocidade)
        elif valor < -velocidade:
            particulas[i].setVelocidade(-velocidade)
        else:
            particulas[i].setVelocidade(valor)

def imprime():
    alvo1 = 0

    for i in range(len(particulas)):
        if particulas[i].valorTotal == alvo:
            alvo1 = i

    if alvo1 < len(particulas):
        print "\n"
    else:
        print "Solucao nao encontrada."
    return

def inicializaParticula():
    for i in range(numeroParticulas):
        novaParticula = Particula(numeroEntradas)
        pesoTotal = sum([i*j for i,j in zip(novaParticula.dados, pesos)])
        novaParticula.melhorParticula = pesoTotal
        particulas.append(novaParticula)

def retornaMinimo():
    minimo = 0
    encontraNovoMinimo = False
    feito = False

    while not feito:
        novoMinimo = False
        for i in range(numeroParticulas):
            if i != minimo:
                if math.fabs(alvo - particulas[i].valorTotal) < math.fabs(alvo - particulas[minimo].valorTotal):
                    if particulas[i].pesoTotal <= pesoMaximo:
                        minimo = i
                        novoMinimo = True
        if novoMinimo == False:
            feito = True
    return minimo

def sigmoid(vid):
    y = 1/(1 + math.exp(-vid))
    return y

def successMessage(executionTime):
    print('Terminou com sucesso em %.2f segundos' % executionTime)

def PSA():
    gMelhor = 0
    gTesteMelhor = 0
    epoca = 0
    passou = numeroParticulas # Particulas que passaram do limite de peso
    feito = False

    print("Inicializando particulas...")
    while passou == numeroParticulas:
        inicializaParticula()
        for i in range(numeroParticulas):
            if particulas[i].pesoTotal <= pesoMaximo:
                passou += 1;

    for i in range(numeroParticulas):
        if particulas[i].pesoTotal <= pesoMaximo:
            gMelhor = i
            break

    while not feito:
        if epoca < numeroEpocas:
            for i in range(numeroParticulas):
                if particulas[i].valorTotal == alvo:
                    feito = True

            gTesteMelhor = retornaMinimo()
            if math.fabs(alvo - particulas[gTesteMelhor].valorTotal) < math.fabs(alvo - particulas[gMelhor].valorTotal):
                if particulas[gTesteMelhor].pesoTotal <= pesoMaximo:
                    gMelhor = gTesteMelhor

            atualizaVelocidade(gMelhor)

            atualizaParticulas(gMelhor)

            # print "\n\n*****  ÉPOCA: "+ str(epoca)
            print "E:-" + str(epoca)+"-peso:-" + str(particulas[gMelhor].pesoTotal) + "-valor:-" + str(particulas[gMelhor].valorTotal) + "-fitness:-" + str(particulas[gMelhor].melhorParticula)
            epoca += 1
        else:
            feito = True
    return

if __name__ == '__main__':
    startTime = timeit.default_timer()

    PSA()
    imprime()

    elapsed = timeit.default_timer() - startTime
    successMessage(elapsed)
