####################################
# helpers.py                       #
#                                  #
# Helper functions for genetic.py  #
#                                  #
# Doug Lloyd                       #
# March 15, 2019                   #
# CS50                             #
####################################

from finished.phrase1 import target
from termcolor import colored

def colorize(s):

    # print characters that match the target in green, else in red
    # only used to help with visualizing the effects of the algorithm over time
    for i in range(len(s)):
        if s[i] == '1':
            print(colored(s[i], "green"), end="")
        else:
            print(colored(s[i], "red"), end="")

def col_score(s):

    # print characters that match the target in green, else in red
    # only used to help with visualizing the effects of the algorithm over time
    if s > 0:
        print(colored(s, "green"), end="")
    else:
        print(colored(s, "red"), end="")


# gen = current generation number, phr = string to print, fit = string's fitness
def summarize(gen, phr, fit, tr):

    # cleanly summarizes the data of the "best we've seen so far"
    print(f"Generation #{gen:4}: ", end="")
    colorize(phr)
    print(f"  score:" , end="")
    col_score(fit)
    print(f" tran: {tr:2}")
