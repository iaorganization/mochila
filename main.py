from AlgoritmoGenetico import AlgoritmoGenetico


if __name__ == '__main__':

	ag = AlgoritmoGenetico(30,10)
	ag.simulaPesos(30,100)
	print ag.pesos
	ag.simulaValores(30,1000)
	print ag.valores
	print "***********  populacao inicial ***************"
	ag.imprimePopulacao()

	ag.calculaFitness()

	for i in range(50000):
		print "\n\n************************  Geracao: {0}".format(i) 
		ag.cruza()	
		ag.muta()
		ag.seleciona()
		# ag.imprimePopulacao()
		best = ag.getMelhorIndividuo()
		print "\nMelhor individuo-> {0} \n".format(ag.getConfiguracaoMochila(best))
	

	