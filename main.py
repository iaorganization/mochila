from AlgoritmoGenetico import AlgoritmoGenetico



def readConfigurationFile(fileName):
	file = open(fileName,"r")
	dados=[]
	for line in file:
		dados.append(line)

	pesos = dados[0]
	pesos = pesos.split(",")
	pesos = map(int,pesos)
	valores = dados[1]
	valores = valores.split(",")
	valores = map(int,valores)
	pesoMaximo = dados[2]
	pesoMaximo = int(pesoMaximo)
	print pesos
	print valores
	print pesoMaximo
	return pesos,valores,pesoMaximo
	# print valores + str(len(valores))

def writeFile(fileName,qtde,rangeMax):
	file2 = open(fileName,"w")
	ag = AlgoritmoGenetico(qtde,1)
	ag.simulaValores(qtde,rangeMax)
	ag.simulaPesos(qtde,rangeMax)
	pesoMaximo=0
	for peso in ag.pesos:
		pesoMaximo+=peso
	print pesoMaximo
	pesoMaximo = int(0.7*pesoMaximo)
	valores = ','.join(str(e) for e in ag.valores)
	pesos = ','.join(str(e) for e in ag.pesos)
	file2.write(pesos+"\n")
	file2.write(valores+"\n")
	file2.write(str(pesoMaximo))
	file2.close()




if __name__ == '__main__':
	# writeFile("mochila2.txt",100,100)
	pesos,valores,pesoMaximo = readConfigurationFile("mochila2.txt")

	ag = AlgoritmoGenetico(len(pesos),10)
	ag.pesos = pesos
	ag.valores = valores
	ag.pesoMaximo = pesoMaximo
	ag.probabilidadeCruzamento = 70
	ag.probabilidadeMutacao = 10
	nrGeracoes = 50000

	
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


