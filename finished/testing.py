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
import random
from cs50 import get_string
import numpy
import math
import pandas as pd
import statistics
import talib
path = "/home/yogesh/Downloads/JAN DATA 2019/JAN/01JAN/SBIN.txt"
df1 = pd.read_csv(path,sep=",",header=None)
df = df1[6]
dfv= df1[7]
avg = statistics.mean(df)
lot_size=500
brokerage=20
# ask the user for a target string
# target = get_string("What target do you want to match? ")
target = 12
#count0 = 0

# threading
# prompt the user for a generation size
popSize = 750#get_int("How many individuals in each generation? ")

# keep track of our population, generation, and the best score we've seen so far
population = "111010001000"
bestScore = -111222
generation = 1
prev_per = 0
siz = 4096

def getFitness(pop):
    transaction = 0
    score = 0
    shares = 0
    buy = 0
    buy_price = 0
    sell = 0
    sell_price = 0
    # r1_avg
    # sel
    # for i in range(len(population)):
    for p in range(len(df) - 20):
        j = p + 20
        count0 = 0
        count0=r1(j,count0)
        count0=r2(j,count0)
        count0=r3(j,count0)
        count0=r4(j,count0)
        count0=r5(j,count0)
        count0=r6(j,count0)
        brokerage = 20
        if count0 > (target / 4):
            if buy == 1 and sell == 0:
                buy = 0
                if ((df[j] - buy_price) * lot_size * 0.06 < 20):
                    brokerage = (df[j] - buy_price) * lot_size * 0.06
                score += ((df[j] - buy_price) * lot_size - brokerage)
                transaction += 1
            elif buy == 0 and buy == 0:
                sell = 1
                sell_price = df[j]
        else:  # if population[2] == '1':
            if sell == 1 and buy == 0:
                sell = 0
                if ((df[j] - buy_price) * lot_size * 0.06 < 20):
                    brokerage = (df[j] - sell_price) * lot_size * 0.06
                score -= ((df[j] - sell_price) * lot_size - brokerage)
                transaction += 1
            elif sell == 0 and buy == 0:
                buy = 1
                buy_price = df[j]
    if sell == 1 and buy == 0:
        sell = 0
        score -= (df[j] - sell_price)
    elif buy == 1 and sell == 0:
        buy = 0
        score += (df[j] - buy_price)

    return score

        # print("sell:"+str(sell)+" buy:"+str(buy)+" sell_p: "+str(sell_price)+" buy_p: "+str(buy_price))


# create a child of two members of the current generation

def r1(j,count0):
    if j > 0:
        close_prices = df[0:j]
        volumes = dfv[0:j]
        rocp = talib.ROCP(close_prices, timeperiod=1)
        norm_volumes = (volumes - numpy.mean(volumes)) / math.sqrt(numpy.var(volumes))
        vrocp = talib.ROCP(norm_volumes + numpy.max(norm_volumes) - numpy.min(norm_volumes), timeperiod=1)
        # vrocp = talib.ROCP(volumes, timeperiod=1)
        #if rocp[j - 1] != numpy.NaN and vrocp[j - 1] != numpy.NaN:
        pv = rocp[j - 1] * vrocp[j - 1] * 100
        if pv > 0:
            if rocp[j - 1] > 0 and vrocp[j - 1] > 0:
                if population[1] == '0':
                    count0 += 1
            elif rocp[j - 1] < 0 and vrocp[j - 1] < 0:
                if population[0] == '0':
                    count0 += 1
    return count0


def r2(j,count0):
    if j > 0:
        avg = statistics.mean(df[j - 20:j])
        if df[j] > avg:
            if population[3] == '0':
                count0 += 1
        elif df[j] < avg:
            if population[2] == '0':
                count0 += 1

    return count0



def r3(j,count0):
    if j > 0:
        rocp = talib.ROCP(df[0:j], timeperiod=1)
        if rocp[j - 1] > 0:
            if population[5] == '0':
                count0 += 1
        elif rocp[j - 1] < 0:
            if population[4] == '0':
                count0 += 1

    return count0


def r4(j,count0):
    if j > 34:
        macd, signal, hist = talib.MACD(df[0:j], fastperiod=12, slowperiod=26, signalperiod=9)
        a = macd[j - 2] - hist[j - 2]
        b = macd[j - 1] - hist[j - 1]
        if a > 0 and b < 0:
            if population[7] == '0':
                count0 += 1
        elif a < 0 and b > 0:
            if population[6] == '0':
                count0 += 1

    return count0


def r5(j,count0):
    if j > 0:
        upperband, middleband, lowerband = talib.BBANDS(df[0:j], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        if upperband[j - 1] < df[j]:
            if population[9] == '0':
                count0 += 1
        elif lowerband[j - 1] > df[j]:
            if population[8] == '0':
                count0 += 1
    return count0


def r6(j,count0):
    if j > 0:
        volumes = dfv[0:j]
        norm_volumes = (volumes - numpy.mean(volumes)) / math.sqrt(numpy.var(volumes))
        vrocp = talib.ROCP(norm_volumes + numpy.max(norm_volumes) - numpy.min(norm_volumes), timeperiod=1)
        if vrocp[j - 1] > 0:
            if population[11] == '0':
                count0 += 1
        elif vrocp[j - 1] < 0:
            if population[10] == '0':
                count0 += 1
    return count0


from finished.phrase1 import target
from termcolor import colored

def colorize(score):

    # print characters that match the target in green, else in red
    # only used to help with visualizing the effects of the algorithm over time

    if score > 0:
        print(colored(score, "green"), end="")
    else:
        print(colored(score, "red"), end="")


# gen = current generation number, phr = string to print, fit = string's fitness
def summarize(phr, score):

    # cleanly summarizes the data of the "best we've seen so far"
    print(f"Rule #{ phr:20}: ", end="")
    colorize(score)

bestScore = getFitness(population)
summarize(population, bestScore)
