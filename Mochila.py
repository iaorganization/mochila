class Mochila(object):

	def __init__(self):
		self.itens = []
		self.pesoMaximo = 0

	def adicionaItem(self, item):
		self.itens.append(item)

	def getNrItens(self):
		tempNrItens = 0
		for i in self.itens:
			tempNrItens += 1
		return tempNrItens

	def getPesoOcupado(self):
		tempPesoOcupado = 0
		for i in self.itens:
			tempPesoOcupado += i.peso
		return tempPesoOcupado

	def getValorAtual(self):
		tempValor = 0.0
		for i in self.itens:
			tempValor += i.valor
		return tempValor

	def removeItem(self, item):
		self.itens.remove(item)

	def setPesoMaximo(self, pesoMaximo):
		self.pesoMaximo = pesoMaximo

class Item(object):

	def __init__(self, peso, valor):
		self.peso = peso
		self.valor = valor
