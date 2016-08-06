from AlgoritmoGenetico import AlgoritmoGenetico
from FileUtils import FileUtils



if __name__ == '__main__':
	util = FileUtils()
	# util.writeConfigurationFile("mochila2.txt",1000,100)
	print "Lendo arquivo de entrada de dados"
	util = FileUtils()
	pesos,valores,pesoMaximo = util.readConfigurationFile("mochila2.txt")

	print "Criando a populacao inicial..."
	ag = AlgoritmoGenetico(len(pesos),10)
	ag.pesos = pesos
	ag.valores = valores
	ag.pesoMaximo = pesoMaximo
	ag.probabilidadeCruzamento = 95
	ag.probabilidadeMutacao = 5
	nrGeracoes = 100000


	
	
	print "***********  populacao inicial    ***************"
	print "calculando o fitness..."
	ag.calculaFitness()
	# ag.populacao[0].setFitness(10.0)
	# ag.populacao[1].setFitness(20.0)
	# ag.populacao[2].setFitness(30.0)
	
	# ag.populacao[3].setFitness(40.0)
	# ag.populacao[4].setFitness(50.0)
	# ag.imprimePopulacao()
	ag.seleciona()

	for i in range(nrGeracoes):
		print "\n\n*************  Geracao: "+ str(i) + "   *************" 
		# print "cruzando"
		ag.cruza()	
		# print "mutando"
		ag.muta()
		# ag.imprimePopulacao()
		# print "\n\n"
		# print "selecionando"
		ag.seleciona()
		# ag.imprimePopulacao()
		# print "coletando melhores individuos"
		print ag.getConfiguracaoMochila(ag.getMelhorIndividuo())
		# ag.imprime_n_melhoresIndividuos(3)


