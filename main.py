from AlgoritmoGenetico import AlgoritmoGenetico


if __name__ == '__main__':

	ag = AlgoritmoGenetico(50,20)
	# ag.simulaPesos(50,100)
	print ag.pesos
	# ag.simulaValores(50,1000)
	print ag.valores
	ag.pesoMaximo = 1500
	ag.probabilidadeCruzamento = 70
	ag.probabilidadeMutacao = 10
	nrGeracoes = 100000

	
	print "***********  populacao inicial    ***************"
	ag.calculaFitness()
	ag.imprimePopulacao()

	for i in range(nrGeracoes):
		print "\n\n*************  Geracao: "+ str(i) + "   *************" 
		ag.cruza()	
		ag.muta()
		ag.seleciona()
		# ag.imprimePopulacao()
		ag.imprime_n_melhoresIndividuos(3)
	

