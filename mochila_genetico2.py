from pyevolve import G2DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
from sklearn import datasets
import math

objetivo=25;
pesos=[1,2,3,5,4,6,8,7,9,10]

def eval_func(chromosome):
    score = 0.0;
    dif=0;
    for i in xrange(chromosome.getHeight()):
        total=0;
        for j in xrange(chromosome.getWidth()):
            total+=chromosome[i][j]*pesos[j];
        dif+=math.fabs(total-(objetivo));
    score=1/(dif+1);
    return score


genome = G2DList.G2DList(3, 10)
genome.setParams(rangemin=0, rangemax=1)

genome.evaluator.set(eval_func)
genome.crossover.set(Crossovers.G2DListCrossoverSingleHPoint)
genome.mutator.set(Mutators.G2DListMutatorIntegerGaussian)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(10)

ga.evolve(freq_stats=100)

ga.bestIndividual()



