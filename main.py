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
	return pesos,valores,pesoMaximo

def writeConfigurationFile(fileName,qtde,rangeMax):
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
	# writeConfigurationFile("mochila2.txt",1000,100)
	print "Lendo arquivo de entrada de dados"
	pesos,valores,pesoMaximo = readConfigurationFile("mochila2.txt")
	print "Criando a populacao inicial..."
	ag = AlgoritmoGenetico(len(pesos),1000)
	ag.pesos = pesos
	ag.valores = valores
	ag.pesoMaximo = pesoMaximo
	ag.probabilidadeCruzamento = 90
	ag.probabilidadeMutacao = 10
	nrGeracoes = 5000

	
	print "***********  populacao inicial    ***************"
	print "calculando o fitness..."
	ag.calculaFitness()
	# ag.imprimePopulacao()

	for i in range(nrGeracoes):
		print "\n\n*************  Geracao: "+ str(i) + "   *************" 
		ag.cruza()	
		ag.muta()
		ag.seleciona()
		# ag.imprimePopulacao()
		ag.imprime_n_melhoresIndividuos(3)


