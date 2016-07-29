from Cromossomo import Cromossomo
import random
from operator import attrgetter

class AlgoritmoGenetico:

		
	def __init__(self,nrGenes,tamanhoPopulacao):
		self.nrGenes = nrGenes
		self.tamanhoPopulacao = tamanhoPopulacao
		self.populacao = self.criaPopulacaoInicial(self.nrGenes)
		self.pesos=		[8, 41, 51, 28, 7, 32, 70, 32, 91, 59, 47, 7, 70, 94, 68, 71, 53, 46, 22, 25, 99, 33, 72, 77, 80, 22, 3, 39, 6, 68, 33, 51, 58, 22, 18, 83, 19, 86, 79, 14, 32, 37, 28, 34, 86, 42, 41, 37, 62, 41]
		self.valores=	[222, 723, 941, 640, 435, 768, 794, 520, 488, 864, 840, 640, 61, 393, 484, 595, 580, 492, 44, 865, 762, 42, 889, 421, 558, 720, 629, 896, 880, 314, 319, 591, 600, 877, 566, 944, 183, 826, 84, 216, 331, 426, 499, 706, 990, 72, 127, 72, 922, 204]
		self.pesoMaximo=1500
		self.probabilidadeCruzamento=70
		self.probabilidadeMutacao=5

	def cruzamentoUmPonto(self,cromo1,cromo2):
		numGenes = len(cromo1.genes)
		pontoCorte = random.randrange(numGenes)
		genes1 = cromo1.genes[0:pontoCorte] + cromo2.genes[pontoCorte:numGenes]
		genes2 = cromo2.genes[0:pontoCorte] + cromo1.genes[pontoCorte:numGenes]
		filho1 = Cromossomo(self.nrGenes)
		filho2 = Cromossomo(self.nrGenes)
		filho1.genes = genes1
		filho2.genes = genes2
		return filho1,filho2


	def mutacao(self,cromossomo):
		for i in range(0,len(cromossomo.genes)):
			prob = random.randrange(100)
			if(prob < self.probabilidadeMutacao):
				if cromossomo.genes[i]==1:
					cromossomo.genes[i]=0
				else:
					cromossomo.genes[i]=1


	def calculaFitness(self):
		for cromossomo in self.populacao:
			pesoTotal=0
			valorTotal=0
			for i in range(0,len(cromossomo.genes)):
				if(cromossomo.genes[i]==1):
					pesoTotal += self.pesos[i]
					valorTotal += self.valores[i]
			if(pesoTotal > self.pesoMaximo):
				cromossomo.setFitness(0)
			else:
				cromossomo.setFitness(0.7*valorTotal-0.3*pesoTotal)


	def criaPopulacaoInicial(self,nrGenes):
		populacao = []
		for i in range(0,self.tamanhoPopulacao):
			cromo = Cromossomo(nrGenes)
			populacao.append(cromo)
		return populacao


	def cruza(self):
		cromossomos=[]
		for cromossomo in self.populacao:
			prob = random.randrange(100)
			if(prob <= self.probabilidadeCruzamento): #verifica se o cromossomo ira para o cruzamento
				cromossomos.append(cromossomo)
		for x in range(0,len(cromossomos),2):
			if (x+1 >= len(cromossomos)):
				break
			f1,f2 = self.cruzamentoUmPonto(cromossomos[x],cromossomos[x+1])
			self.populacao.append(f1)
			self.populacao.append(f2)


	def seleciona(self):
		self.calculaFitness()
		novaPopulacao=[]
		best = self.getMelhorIndividuo()					# 
		novaPopulacao.append(best)							# elitismo
		for i in range(self.tamanhoPopulacao):
			c1 = random.randrange(len(self.populacao))
			c2 = random.randrange(len(self.populacao))
			cromossomoVencedor = self.torneio(self.populacao[c1],self.populacao[c2])
			if cromossomoVencedor not in novaPopulacao:
				novaPopulacao.append(cromossomoVencedor)
		self.populacao = novaPopulacao


	def torneio(self,cromossomo1,cromossomo2):
		if(cromossomo1.getFitness > cromossomo2.getFitness):
			return cromossomo1
		else:
			return cromossomo2

	def muta(self):
		best = self.getMelhorIndividuo()
		for cromossomo in self.populacao:
			if(id(best) != id(cromossomo)): #nao executa mutacao no melhor individuo
				self.mutacao(cromossomo)

	
	def imprimePopulacao(self):
		print len(self.populacao)
		for cromossomo in self.populacao:
			print cromossomo.toString() + " " + self.getConfiguracaoMochila(cromossomo)


	def getConfiguracaoMochila(self,cromossomo):
		pesoTotal = 0
		valorTotal = 0
		for i in range(0,len(cromossomo.genes)):
			if(cromossomo.genes[i]==1):
				pesoTotal += self.pesos[i]
				valorTotal += self.valores[i]
		return "peso: " + str(pesoTotal)+", valor: "+ str(valorTotal)


	def getMelhorIndividuo(self):
		return max(self.populacao, key=attrgetter('fitness'))


	def simulaPesos(self,qtdeItens, maxPeso):
		self.pesos = []
		for i in range(0,qtdeItens):
			self.pesos.append(random.randrange(maxPeso)) 

	def simulaValores(self,qtdeItens,maxValor):
		self.valores=[]
		for i in range(0,qtdeItens):
			self.valores.append(random.randrange(maxValor)) 

	def get_n_melhorsIndividuos(self,n):
		listaOrdenada = sorted(self.populacao, key=lambda x: x.fitness,reverse = True)
		return listaOrdenada[0:n]

	def imprime_n_melhoresIndividuos(self,n):
		listaMelhoresIndividuos = self.get_n_melhorsIndividuos(n)
		for cromossomo in listaMelhoresIndividuos:
			print self.getConfiguracaoMochila(cromossomo)




