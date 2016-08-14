# -*- coding: utf-8 -*-

from AlgoritmoGenetico2 import AlgoritmoGenetico
from FileUtils import FileUtils
from Mochila import Item
from Mochila import Mochila
import os
import random
import sys
import timeit


class AGMain(object):

    def __init__(self):
        self.configuracoesMochila = [] # lista de configuracoes das mochilas (contem os itens com seus pesos e valores)
        self.itensDisponiveis = []
        self.fileUtils = FileUtils()

    def errorMessage(self):
        print("\nErro: argumentos incorretos."
            + "\nModo correto: $ python main.py gerações pontos_corte peso_maximo"
            + "\n\n\t\tgeracoes: número de gerações"
            + "\n\t\tpontos_corte: número de pontos de corte do cruzamento"
            + "\n\t\tpeso_maximo: quantidade de peso que a mochila suporta"
            + "\n\nExemplo: $ python main.py 10000 2 30000")

    def successMessage(self, executionTime):
        print('Terminou com sucesso em %.2f segundos' % executionTime)

    def main(self):
        os.system("clear")

        # gera itens aleatorios e grava em itens.csv
        if len(sys.argv) == 3:
            fileName = sys.argv[1]
            nrItens = int(sys.argv[2])
            self.itensDisponiveis = self.fileUtils.generateRandomItens(nrItens, 100, 100)
            self.fileUtils.writeItensFile(self.itensDisponiveis, fileName)

        # roda algoritmo lendo o arquivo itens.csv
        elif len(sys.argv) == 4:
            startTime = timeit.default_timer()

            nrGeracoes = int(sys.argv[1])
            qtdePontosCruzamento = int(sys.argv[2])
            pesoMaximo = int(sys.argv[3])

            print "Configurado para %d gerações, %d pontos de cruzamento e mochila com peso máximo %d" %(nrGeracoes, qtdePontosCruzamento, pesoMaximo)
            print "Lendo arquivo de entrada de dados..."
            self.itensDisponiveis = self.fileUtils.readItensFromFile("itens.csv")

            print "Criando a populacao inicial..."
            ag = AlgoritmoGenetico(len(self.itensDisponiveis), 100)
            ag.pesos = [item.peso for item in self.itensDisponiveis]
            ag.valores = [item.valor for item in self.itensDisponiveis]
            ag.pesoMaximo = pesoMaximo
            ag.probabilidadeCruzamento = 95
            ag.probabilidadeMutacao = 5

            print "\n***** POPULAÇÃO INICIAL"
            ag.calculaFitness()

            for i in range(nrGeracoes):
                print "\n\n*****  GERAÇÃO: " + str(i + 1)
                ag.cruza(qtdePontosCruzamento)
                ag.muta()
                ag.seleciona()
                tempPesos, tempValores = ag.getMelhoresPesosValores(ag.getMelhorIndividuo())
                self.configuracoesMochila.append(Mochila(tempPesos, tempValores))
                print ag.getConfiguracaoMochila(ag.getMelhorIndividuo())

            ultimaMochila = self.configuracoesMochila[nrGeracoes - 1]
            tempFile = open("ultimaMochila.csv", "w")
            tempFile.write("GERAÇÃO: " + str(nrGeracoes)
                + "\nPESO TOTAL: " + str(ultimaMochila.getPesoOcupado())
                + "\nVALOR TOTAL: " + str(ultimaMochila.getValorTotal())
                + "\nQUANTIDADE DE ITENS: " + str(ultimaMochila.getNrItens())
                + "\nLISTA DE ITENS (NUMERO, PESO, VALOR):\n")

            for index, item in enumerate(ultimaMochila.itens):
                tempFile.write(str(index) + ", " + str(item.peso) + ", " + str(item.valor) + "\n")
            tempFile.close()

            elapsed = timeit.default_timer() - startTime
            self.successMessage(elapsed)

        else:
            self.errorMessage()

if __name__ == '__main__':
    agm = AGMain()
    agm.main()
