# -*- coding: utf-8 -*-

from Mochila import Item
import random
from AlgoritmoGenetico import AlgoritmoGenetico

class FileUtils(object):

    def __init__(self):
        pass

    def generateRandomItens(self, nrItens, pesoMaximoUnitario, valorMaximmoUnitario):
        """ Gera itens com pesos e valores aleatórios.

            Args:
                nrItens: número de itens a ser gerado aleatóriamente
                pesoMaximoUnitário: peso máximo que cada item pode ter
                valorMaximoUnitário: valor máximo que cada item pode ter

            Returns:
                itensDisponiveis: uma lista com os itens gerados
        """
        itensDisponiveis = [] # apaga todos os itens disponíveis
        for i in range(nrItens):
            tempPeso = random.randrange(1, pesoMaximoUnitario)
            tempValor = random.randrange(1, valorMaximmoUnitario)
            item = Item(tempPeso, tempValor)
            itensDisponiveis.append(item)
        return itensDisponiveis

    def readConfigurationFile(self, fileName):
        tempFile = open(fileName,"r")
        dados=[]
        for line in tempFile:
            dados.append(line)

        pesos = dados[0]
        pesos = pesos.split(",")
        pesos = map(int,pesos)
        valores = dados[1]
        valores = valores.split(",")
        valores = map(int,valores)
        pesoMaximo = dados[2]
        pesoMaximo = int(pesoMaximo)

        tempFile.close()
        return pesos, valores, pesoMaximo

    def readItensFromFile(self, fileName):
        """ Lê itens de um arquivo csv e insere em itensDisponiveis.
            Cada linha representa um item (peso, valor).

            Args:
                fileName: nome do arquivo contendo os itens

            Returns:
                itensDisponiveis: uma lista de objetos da classe Item
        """
        itensDisponiveis = [] # reseta itens disponíveis
        tempFile = open(fileName)
        linhas = [linha.strip() for linha in tempFile]

        for linha in linhas:
            elementos = linha.split(",")
            peso = int(elementos[0])
            valor = int(elementos[1])
            itensDisponiveis.append(Item(peso,valor))

        tempFile.close()

        return itensDisponiveis

    def writeConfigurationFile(self, fileName, qtde, rangeMax):
        tempFile = open(fileName,"w")
        ag = AlgoritmoGenetico(qtde, 1)
        ag.simulaValores(qtde, rangeMax)
        ag.simulaPesos(qtde, rangeMax)
        pesoMaximo = 0
        for peso in ag.pesos:
            pesoMaximo += peso
        print pesoMaximo
        pesoMaximo = int(0.7 * pesoMaximo)
        valores = ','.join(str(e) for e in ag.valores)
        pesos = ','.join(str(e) for e in ag.pesos)
        tempFile.write(pesos + "\n")
        tempFile.write(valores + "\n")
        tempFile.write(str(pesoMaximo))
        tempFile.close()

    def writeItensFile(self, itensDisponiveis, fileName):
        """ Grava itens em um arquivo.
            O formato do arquivo é csv.
            Um item por linha, sendo representado por 'peso, valor'.

            Args:
                itensDisponiveis: lista de itens a ser gravada em um arquivo
                fileName: nome do arquivo
        """
        tempFile = open(fileName,"w")
        for i in itensDisponiveis:
            tempFile.write(str(i.peso) + "," + str(i.valor) + "\n")
        tempFile.close()