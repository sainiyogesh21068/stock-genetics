####################################
# genetic.py                       #
#                                  #
# Script to run genetic algorithm  #
#                                  #
# Doug Lloyd                       #
# March 15, 2019                   #
# CS50                             #
####################################

import random

from finished.phrase1 import Phrase
from finished.helpers import summarize
from sklearn.preprocessing import MinMaxScaler
# threading
# prompt the user for a generation size
popSize = 100#get_int("How many individuals in each generation? ")

# keep track of our population, generation, and the best score we've seen so far
population = []
bestScore = -111222
generation = 1
prev_per = 0
lot_size=500
siz = 4096*4
# initial population from which other generations will follow
for i in range(popSize):
    population.append(Phrase())

child_set = set([])
# keep going until we've found the target string
while generation<10:

    # assess the fitness of each member of the population
    for i in range(popSize):
        population[i].getFitness()
        hash=''
        pre=len(child_set)
        child_set.add(population[i].getContents())
        now=len(child_set)
        if pre!=now:
            #print(now)
            per = (now/siz) * 50
            per = int(per)
            if per!=prev_per:
                for j in range(per):
                    hash+='#'
                for j in range(50-per):
                    hash+='.'
                print(hash + "\t" + str(now) + "/" + str(siz))
            prev_per=per
        # if it's the best we've seen so far, let's report on it
        if int(population[i].score) > int(bestScore):
            bestScore = population[i].score
            summarize(generation, population[i].getContents(), bestScore, population[i].transaction)

    # create the mating pool for the next generation
    matingPool = []

    # clear the population array, but save the parents
    parents = population[:]
    population = []

    # for each one of the parents, add it to the mating pool more often if
    # its fitness is higher
    data=[]
    parents_sorted=parents
    parents_sorted.sort(key= lambda x:x.score, reverse=True)
    for i in range(len(parents)):
        data.append([parents_sorted[i].score,0])
    scaler=MinMaxScaler(feature_range=(0,5))
    scaler.fit(data)
    # MinMaxScaler(copy=True, feature_range=(0, 5))
    data_scaled=scaler.transform(data)
    for i in range(popSize):
        for k in range(2):
            matingPool.append(parents_sorted[i])
            if(len(matingPool)>popSize):
                break
        if(len(matingPool)>popSize):
            break

    # build the next generation
    for i in range(popSize):

        # arbitrarily choose two parents from the mating pool
        parentA = random.choice(matingPool)
        parentB = random.choice(matingPool)

        # crossover/breed those two parents together
        child = parentA.crossover(parentB)

        # small chance that some characters in the child may mutate
        child.mutate()

        # add the child to the next generation's population
        population.append(child)

    # done assessing the current generation
    #prev_gen=generation
    generation += 1
    #new_gen=generation
    #if prev_gen!=new_gen:

    print("Generation #\t" +str(generation) +":")

