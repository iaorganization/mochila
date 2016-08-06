import itertools
import random


class Cromossomo:

	newid = itertools.count().next

	def __init__(self, nrGenes, lista=[]):
		self.id = Cromossomo.newid()
		self.fitness = 0
		self.genes = lista
		self.nrGenes = nrGenes
		self.inicializa()

	def inicializa(self):
		if len(self.genes) == 0:
			for i in range(0,self.nrGenes):
				self.genes.append(random.randrange(2))

	def setFitness(self,valor):
		self.fitness = valor

	def getFitness(self):
		return self.fitness

	def __repr__(self):
		return ': '.join(['Genes', str(self.genes), 'Fitness', str(self.fitness), 'ID', str(self.id)])

	def toString(self):
		return "Genes: " + str(self.genes) + ", Fitness:" +  str(self.fitness) + ", ID: " + str(self.id)
