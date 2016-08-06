# -*- coding: utf-8 -*-

from AlgoritmoGenetico2 import AlgoritmoGenetico
import os
import sys
import timeit


class AGMain(object):

    def __init__(self):
        pass

    def __print_error_message(self):
        print('\nErro: argumentos incorretos.\n\n\tModo correto: $ python main.py gerações pontos_corte\n\n\t\tgeracoes: número de gerações\n\t\tpontos_corte: número de pontos de corte do cruzamento\n\n\tExemplo: $ python main.py 10000 2\n')

    def __print_success_message(self, execution_time):
        print('Terminou com sucesso em %.2f segundos' % execution_time)

    def readConfigurationFile(self, fileName):
        tempFile = open(fileName, "r")
        dados = []
        for line in tempFile:
            dados.append(line)

        pesos = dados[0]
        pesos = pesos.split(",")
        pesos = map(int, pesos)
        valores = dados[1]
        valores = valores.split(",")
        valores = map(int, valores)
        pesoMaximo = dados[2]
        pesoMaximo = int(pesoMaximo)

        tempFile.close()
        return pesos, valores, pesoMaximo

    def writeConfigurationFile(self, fileName, qtde, rangeMax):
        tempFile = open(fileName, "w")
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

    def main(self):
        os.system('clear')

        if len(sys.argv) == 3:
            start_time = timeit.default_timer()

            nrGeracoes = int(sys.argv[1])
            qtdePontosCruzamento = int(sys.argv[2])
            print "Configurado para %d gerações e %d pontos de cruzamento" %(nrGeracoes, qtdePontosCruzamento)

            print "Lendo arquivo de entrada de dados..."
            pesos, valores, pesoMaximo = self.readConfigurationFile("mochila2.txt")

            print "Criando a populacao inicial..."
            ag = AlgoritmoGenetico(len(pesos), 100)
            ag.pesos = pesos
            ag.valores = valores
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
                print ag.getConfiguracaoMochila(ag.getMelhorIndividuo())

            elapsed = timeit.default_timer() - start_time
            self.__print_success_message(elapsed)
        else:
            self.__print_error_message()

if __name__ == '__main__':
    agm = AGMain()
    agm.main()
