""" guess number rules. """
import random
from collections import namedtuple


def genQuestion(amount):
    """ check entered then return random number string. """
    if not isinstance(amount, int):
        return (False, "The number you entered is not specified.")
    elif amount > 10:
        return (False, "The number you entered is out of range.")
    else:
        sample = '0123456789'
        genNumList = random.shuffle(random.sample(sample, amount))
        return (True, "".join(genNumList))

def isMatchAnswer(guess, answer):
    """
    number is in answer list but in wrong position, B + 1.
    number is in answer list and in correct position, A + 1.
    """
    if not isinstance(guess, str) or not isinstance(answer, str):
        return (False, "The number you entered is not specified.")
    elif len(guess) != len(answer):
        return (False, "The number you entered is out of range.")
    else:
        abList = [0, 0]
        guessList = list(guess)
        answerList = list(answer)
        for element in guessList:
            if element in answerList:
                resultElement = 0 if guessList.index(element) == answerList.index(element) else 1
                abList[resultElement] += 1
        result = namedtuple('result', 'A B')
        return (True, result(abList[0], abList[1]))
