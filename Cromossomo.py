import random
import itertools

class Cromossomo:
	newid = itertools.count().next
	def __init__(self,nrGenes):
		self.id = Cromossomo.newid()
		self.fitness = 0
		self.genes = []
		self.nrGenes = nrGenes
		self.inicializa()

	def inicializa(self):
		for i in range(0,self.nrGenes):
			self.genes.append(random.randrange(2))

	def setFitness(self,valor):
		self.fitness = valor

	def getFitness(self):
		return self.fitness

	def toString(self):
		return "genes: " + str(self.genes)+", fitness:" +  str(self.fitness)+", id: " + str(self.id)


