# -*- coding: utf-8 -*-

from AlgoritmoGenetico2 import AlgoritmoGenetico
from Mochila import Item
from Mochila import Mochila
import os
import random
import sys
import timeit


class AGMain(object):

    def __init__(self):
        self.mochila = Mochila()
        self.itensDisponiveis = []

    def errorMessage(self):
        print("\nErro: argumentos incorretos."
            + "\nModo correto: $ python main.py gerações pontos_corte peso_maximo"
            + "\n\n\t\tgeracoes: número de gerações"
            + "\n\t\tpontos_corte: número de pontos de corte do cruzamento"
            + "\n\t\tpeso_maximo: quantidade de peso que a mochila suporta"
            + "\n\nExemplo: $ python main.python 10000 2 30000")

    def generateRandomItens(self, nrItens, pesoMaximoUnitario, valorMaximmoUnitario):
        """ Gera itens com pesos e valores aleatórios.
            Preenche self.itensDisponiveis com os itens gerados.

            Args:
                nrItens: número de itens a ser gerado aleatóriamente
                pesoMaximoUnitário: peso máximo que cada item pode ter
                valorMaximoUnitário: valor máximo que cada item pode ter
        """
        self.itensDisponiveis = [] # apaga todos os itens disponíveis
        for i in range(nrItens):
            tempPeso = random.randrange(1, pesoMaximoUnitario)
            tempValor = random.randrange(1, valorMaximmoUnitario)
            item = Item(tempPeso, tempValor)
            self.itensDisponiveis.append(item)

    def readItensFromFile(self, fileName):
        """ Lê itens de um arquivo csv e insere em self.itensDisponiveis
            A lista se itens disponíveis é resetada, antes de qualquer procecimento

            Args:
                fileName: nome do arquivo contendo os itens

            Notes:
                cada linha representa um item (peso, valor)
        """
        self.itensDisponiveis = [] # reseta itens disponíveis
        tempFile = open(fileName)
        linhas = [linha.strip() for linha in tempFile]
        for linha in linhas:
            elementos = linha.split(",")
            peso = int(elementos[0])
            valor = int(elementos[1])
            self.itensDisponiveis.append(Item(peso,valor))
        tempFile.close()

    def successMessage(self, execution_time):
        print('Terminou com sucesso em %.2f segundos' % execution_time)

    def writeItensFile(self, fileName):
        tempFile = open(fileName,"w")
        for i in self.itensDisponiveis:
            tempFile.write(str(i.peso) + "," + str(i.valor) + "\n")
        tempFile.close()

    def main(self):
        os.system("clear")

        # gera itens aleatorios e grava em itens.csv
        if len(sys.argv) == 2:
            self.generateRandomItens(1000, 100, 100)
            self.writeItensFile(sys.argv[1])

        # roda algoritmo lendo o arquivo itens.csv
        elif len(sys.argv) == 4:
            start_time = timeit.default_timer()

            nrGeracoes = int(sys.argv[1])
            qtdePontosCruzamento = int(sys.argv[2])
            pesoMaximo = int(sys.argv[3])

            print "Configurado para %d gerações, %d pontos de cruzamento e mochila com peso máximo %d" %(nrGeracoes, qtdePontosCruzamento, pesoMaximo)

            self.mochila.setPesoMaximo(pesoMaximo)

            print "Lendo arquivo de entrada de dados..."
            self.readItensFromFile("itens.csv")

            print "Criando a populacao inicial..."
            ag = AlgoritmoGenetico(len(self.itensDisponiveis), 100)
            ag.pesos = [item.peso for item in self.itensDisponiveis]
            ag.valores = [item.valor for item in self.itensDisponiveis]
            ag.pesoMaximo = self.mochila.pesoMaximo
            ag.probabilidadeCruzamento = 95
            ag.probabilidadeMutacao = 5

            print "\n***** POPULAÇÃO INICIAL"
            ag.calculaFitness()

            for i in range(nrGeracoes):
                print "\n\n*****  GERAÇÃO: " + str(i + 1)
                ag.cruza(qtdePontosCruzamento)
                ag.muta()
                ag.seleciona()
                print ag.getConfiguracaoMochila(ag.getMelhorIndividuo())

            elapsed = timeit.default_timer() - start_time
            self.successMessage(elapsed)

        else:
            self.errorMessage()

if __name__ == '__main__':
    agm = AGMain()
    agm.main()
