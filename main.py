from AlgoritmoGenetico import AlgoritmoGenetico
from FileUtils import FileUtils



if __name__ == '__main__':
	util = FileUtils()
	# util.writeConfigurationFile("mochila2.txt",1000,100)
	print "Lendo arquivo de entrada de dados"
	pesos,valores,pesoMaximo = util.readConfigurationFile("mochila2.txt")

	print "Criando a populacao inicial..."
	ag = AlgoritmoGenetico(len(pesos),6)
	ag.pesos = pesos
	ag.valores = valores
	ag.pesoMaximo = pesoMaximo
	ag.probabilidadeCruzamento = 95
	ag.probabilidadeMutacao = 5
	nrGeracoes = 100000


	
	
	print "***********  populacao inicial    ***************"
	print "calculando o fitness..."
	ag.calculaFitness()
	print "selecionando..."
	ag.seleciona()

	for i in range(nrGeracoes):
		print "\n\n*************  Geracao: "+ str(i) + "   *************" 
		ag.cruza()	
		ag.muta()
		ag.seleciona()
		print ag.getConfiguracaoMochila(ag.getMelhorIndividuo())

