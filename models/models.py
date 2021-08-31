from Compiler.mpc_math import log_fx
from Compiler.mpc_math import cos
from Compiler.mpc_math import sin
from Compiler.mpc_math import sqrt
from Compiler.types import *
from Compiler.library import *

import math


e = math.e


class model():

    def __init__(self):
        # TODO: Figure out the best way to implement the layers
        pass

    # Reads model params into a tensor
    def read(self, raw_model):
        pass

    # Classify data
    def classify(self):
        pass


def sig(x):
    if x < -0.5:
        return 0
    if x > 0.5:
        return 1
    return x + 0.5


def true_sig(x):
    return 1 / (1 + 1 / (e ** x))


def dp(a, b):
    # print(a)
    # print(len(a))
    # print(len(b))
    assert (len(a) == len(b))

    res = 0

    for i in range(len(a)):
        res += a[i] * b[i]

    return res


class logistic_regression(model):
    """ Class that allows us to read, and classify with a logistic regression model."""

    def __init__(self, data, raw_model):
        """Constructor."""

        # Example of how to call parents constructor (you don't have to use it if you don't feel a need for it)
        super().__init__()

        # Example of how to make a field variable
        self.sample_size = data.len()
        self.data = data
        self.b = raw_model[0]
        # TODO: Test to make sure the Array is correctly initialized
        self.W = raw_model[1:]


    def classify(self):
        """method takes a 2D list of data and classifies each row as a positive (1) or negative (0) example.
            :return a list containing the classification of each sample of data"""

        sample_size = self.sample_size
        data = self.data
        global b
        b = sfix._new(self.b)
        W = self.W

        classifications = sfix.Array(sample_size)

        @for_range(sample_size)
        def _(i):
            global b
            row = data[i]
            classification_intermediate = dp(W, row) + b
            classification = sig(classification_intermediate)
            classifications[i] = classification

        return classifications


class CNN(model):
    pass
