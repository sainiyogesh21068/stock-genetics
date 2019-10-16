####################################
# phrase.py                        #
#                                  #
# Defines Phrase class for genetic #
#                                  #
# Doug Lloyd                       #
# March 15, 2019                   #
# CS50                             #
####################################

import random
import numpy,math
from cs50 import get_string
import pandas as pd
import statistics
import talib
import os
from termcolor import colored

class Phrase:

    # constructor method
    def __init__(self, contents):
        self.characters = []
        # append len(target) number of randomly chosen printable ASCII chars
        for i in range(len(contents)):
            character = contents[i]
            self.characters.append(character)
        self.r1_avg_p = statistics.mean(df)
        self.count0 = 0
        # self.r1_avg_p = statistics.mean(df)
            # else:
            #     self.characters.append('0')

            # else:
            #     self.characters.append('0')

    # render the character array as a string instead of an array of chars
    def getContents(self):
        return ''.join(self.characters)
        # score the current entity's fitness by counting matches to target
    def getFitness(self):
        self.score = 0
        self.shares = 0
        self.buy = 0
        self.buy_price = 0
        self.sell = 0
        self.sell_price = 0
        self.transaction = 0

        for p in range(len(df) - 21):

            j = p + 20
            self.count0 = 0
            self.r1(j)
            self.r2(j)
            self.r3(j)
            self.r4(j)
            self.r5(j)
            self.r6(j)
            self.r7(j)
            brokerage = 40

            #stoploss

            if self.buy == 1 and self.sell == 0 and ((df[j] - self.buy_price)/self.buy_price)*100 < (-0.5):
                # print("stoploss triggered")
                self.buy = 0
                if ((df[j] + self.buy_price) * lot_size * 0.06 < 40):
                    brokerage = (df[j] + self.buy_price) * lot_size * 0.06
                self.score += ((df[j] - self.buy_price) * lot_size - brokerage)
                self.transaction += 1


            if self.buy == 0 and self.sell == 1 and ((self.sell_price-df[j])/self.sell_price)*100 < (-0.5):
                # print("stoploss triggered")
                self.sell = 0
                if ((df[j] + self.sell_price) * lot_size * 0.06 < 40):
                    brokerage = (df[j] + self.sell_price) * lot_size * 0.06
                self.score = self.score + ((self.sell_price - df[j]) * lot_size) - brokerage
                self.transaction += 1

            brokerage = 40
            if self.count0 > int(target / 4):

                if self.buy == 1 and self.sell == 0:
                    self.buy = 0
                    if ((df[j] + self.buy_price) * lot_size * 0.06 < 40):
                        brokerage = (df[j] + self.buy_price) * lot_size * 0.06
                    self.score += ((df[j] - self.buy_price) * lot_size - brokerage)
                    self.transaction += 1
                    # print(self.characters,self.transaction)

                elif self.sell == 0 and self.buy == 0:
                    self.sell = 1
                    self.sell_price = df[j]


            elif self.count0 < int(target / 4):  # if self.characters[2] == '1':

                if self.sell == 1 and self.buy == 0:
                    self.sell = 0
                    if ((df[j] + self.sell_price) * lot_size * 0.06 < 40):
                        brokerage = (df[j] + self.sell_price) * lot_size * 0.06
                    self.score = self.score + ((self.sell_price-df[j]) * lot_size) - brokerage
                    self.transaction += 1
                    # print(self.characters, self.transaction)

                elif self.sell == 0 and self.buy == 0:
                    self.buy = 1
                    self.buy_price = df[j]


        brokerage = 40

        if self.sell == 1 and self.buy == 0:
            self.sell = 0
            if ((df[j] + self.sell_price) * lot_size * 0.06 < 40):
                brokerage = (df[j] + self.sell_price) * lot_size * 0.06
            self.score = self.score + ((self.sell_price-df[j]) * lot_size) - brokerage
            self.transaction+=1;


        elif self.buy == 1 and self.sell == 0:
            self.buy = 0
            if ((df[j] + self.buy_price) * lot_size * 0.06 < 40):
                brokerage = (df[j] + self.buy_price) * lot_size * 0.06
            self.score += ((df[j] - self.buy_price) * lot_size - brokerage)
            self.transaction+=1
                # print("sell:"+str(self.sell)+" buy:"+str(self.buy)+" sell_p: "+str(self.sell_price)+" buy_p: "+str(self.buy_price))
    # create a child of two members of the current generation
    def crossover(self, partner):

        # create a spot for the characters to go
        child = Phrase()

        # flip a coin for each character, selecting from one parent each time
        for i in range(len(self.characters)):
            if random.random() < 0.5:
                child.characters[i] = self.characters[i]

        return child

    # some portion of the time, need some characters to randomly change
    def mutate(self):

        # less than 1% of the time, change a character into something else
        for i in range(len(self.characters)):
            # if i % 3 != 0:
            if random.random() < 0.03:
                self.characters[i] = chr(random.choice(range(48,50)))
    def r1(self, j):
        if j>0:
            avg = 281.840916666667
            if df[j] > avg:
                if self.characters[1] == '0':
                    self.count0 += 1
            elif df[j] < avg:
                if self.characters[0] == '0':
                    self.count0 += 1

    def r2(self, j):
        if j > 0:
            avg = statistics.mean(df[j-20:j])
            if df[j] > avg :
                if self.characters[3] == '0':
                    self.count0 += 1
            elif df[j] < avg:
                if self.characters[2] == '0':
                    self.count0 += 1

    def r3(self, j):
        if j > 0:
            rocp = talib.ROCP(df[0:j], timeperiod=1)
            if rocp[j-1] > 0:
                if self.characters[5] == '0':
                    self.count0 += 1
            elif rocp[j-1] < 0:
                if self.characters[4] == '0':
                    self.count0 += 1

    def r4(self,j):
        if j > 34:
            macd, signal, hist = talib.MACD(df[0:j], fastperiod=12, slowperiod=26, signalperiod=9)
            a = macd[j-2] - hist[j-2]
            b = macd[j-1] - hist[j-1]
            if a > 0 and b < 0:
                if self.characters[7] == '0':
                    self.count0 += 1
            elif a < 0 and b > 0:
                if self.characters[6] == '0':
                    self.count0 += 1

    def r5(self, j):
        if j > 0:
            upperband, middleband, lowerband = talib.BBANDS(df[0:j], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            if upperband[j-1] < df[j]:
                if self.characters[9] == '0':
                    self.count0 += 1
            elif lowerband[j-1] > df[j]:
                if self.characters[8] == '0':
                    self.count0 += 1

    def r6(self, j):
        if j > 0:
            volumes = dfv[0:j]
            norm_volumes = (volumes - numpy.mean(volumes)) / math.sqrt(numpy.var(volumes))
            vrocp = talib.ROCP(norm_volumes + numpy.max(norm_volumes) - numpy.min(norm_volumes), timeperiod=1)
            if vrocp[j - 1] > 0:
                if self.characters[11] == '0':
                    self.count0 += 1
            elif vrocp[j - 1] < 0:
                if self.characters[10] == '0':
                    self.count0 += 1

    def r7(self,j):
        if (j > 20):
            rsi = talib.RSI(df[0:j], timeperiod=6)
            # macd, signal, hist = talib.MACD((df[0:j]), fastperiod=12, slowperiod=26, signalperiod=9)
            # print(str(a) +" "+ str(b))
            if rsi[j-1] > 70:
                # print(str(a) + str(b))
                if self.characters[13] == '0':
                    self.count0 += 1
            elif rsi[j-1] < 30:
                # print(str(a) + str(b))
                if self.characters[12] == '0':
                    self.count0 += 1


if __name__ == "__main__":
    exit="0"
    #while exit=="0":
    # rule = input("Rule : ")
    mot="JAN"
    DIR = os.listdir("/home/yogesh/Downloads/"+mot+" 2019/"+mot)
    DIR.sort()
    # rule = "11000011100010"
    # i= input("DIR : ")
    total_score=0
    for i in DIR:
        print(i,end="")
        print("\t",end="")
        df1 = pd.read_csv("/home/yogesh/Downloads/"+mot+" 2019/"+mot+"/"+str(i)+"/SBIN.txt", sep=",", header=None)

        df = pd.DataFrame(df1[180:376])
        df = pd.DataFrame(df[6])
        df = df.reset_index()
        df.drop(df.columns[0], inplace=True, axis=1)
        df=df[6]
        dfv = pd.DataFrame(df1[1:376])
        dfv = pd.DataFrame(dfv[7])
        dfv = dfv.reset_index()
        dfv.drop(dfv.columns[0], inplace=True, axis=1)
        dfv=dfv[7]
        if df[1]<df[180]:
            rule="11011000111001"
        elif df[1]>=df[180]:
            rule="10000010000010"
        # ask the user for a target string
        # target = get_string("What target do you want to match? ")111010001000
        target = 14
        popSize = 100
        lot_size = 500
        # rule = "10011110101100"
        ph = Phrase(rule)
        ph.getFitness()
        if ph.score > 0:
            print(colored(ph.score, "green"),end="")
        else:
            print(colored(ph.score, "red"),end="")
        total_score +=ph.score
        print("\t" + str(ph.transaction) + "\t")
    print("Total Score : ",end=" ")
    if total_score > 0:
        print(colored(total_score, "green"), end="")
    else:
        print(colored(total_score, "red"), end="")