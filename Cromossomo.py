import itertools
import random


class Cromossomo(object):

	newid = itertools.count().next

	def __init__(self, nrGenes, lista=None):
		self.id = Cromossomo.newid()
		self.fitness = 0
		self.genes = lista
		self.nrGenes = nrGenes
		self.inicializa()

	def inicializa(self):
		if self.genes == None:
			self.genes = []
			for i in range(0, self.nrGenes):
				tempValor = random.randrange(2)
				self.genes.append(tempValor)

	def setFitness(self,valor):
		self.fitness = valor

	def getFitness(self):
		return self.fitness

	def __repr__(self):
		pass
		# return ': '.join('Fitness', str(self.fitness), 'ID', str(self.id)])

	def toString(self):
		# return ", Fitness:" +  str(self.fitness) + ", ID: " + str(self.id)
		return "Genes: " + str(self.genes) + ", Fitness:" +  str(self.fitness) + ", ID: " + str(self.id)


