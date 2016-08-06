# -*- coding: utf-8 -*-

class Mochila(object):

	def __init__(self, pesos=[], valores=[]):
		self.itens = []
		self.pesoMaximo = 0
		self.inicializa(pesos, valores)

	def inicializa(self, pesos, valores):
		""" Adiciona uma configuracao de pesos e valores à mochila.

			Args:
				pesos: lista de pesos dos itens
				valores: lista de valores dos itens
		"""
		if len(pesos) > 0 and len(valores) > 0:
			nrItens = len(pesos)
			for i in range(nrItens):
				self.adicionaItem(Item(pesos[i], valores[i]))

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

	def getValorTotal(self):
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
