from AlgoritmoGenetico import AlgoritmoGenetico


if __name__ == '__main__':

	ag = AlgoritmoGenetico(10,20)
	ag.simulaPesos(10,100)
	print ag.pesos
	ag.simulaValores(10,1000)
	print ag.valores
	print "***********  populacao inicial ***************"
	ag.calculaFitness()
	ag.imprimePopulacao()

	

	for i in range(50000):
		print "\n\n************************  Geracao: {0}".format(i) 
		ag.cruza()	
		ag.muta()
		ag.seleciona()
		ag.imprimePopulacao()
		best = ag.getMelhorIndividuo()
		print "\nMelhor individuo-> {0} \n".format(ag.getConfiguracaoMochila(best))
	

	