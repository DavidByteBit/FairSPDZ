from Compiler.mpc_math import log_fx
from Compiler.mpc_math import cos
from Compiler.mpc_math import sin
from Compiler.mpc_math import sqrt
from Compiler.types import *
from Compiler.library import *

import math
import json

e = math.e


class model():

    def __init__(self, all_metadata, model_owner_id):
        self.all_metadata = all_metadata
        self.model_owner_id = model_owner_id


    # Reads model params into a tensor
    def read(self, raw_model):
        pass

    # Classify data
    def classify(self):
        pass



def sig(x):
    a = x < -0.5
    b = x > 0.5
    return a.if_else(0, b.if_else(1, 0.5 + x))


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

    def __init__(self, all_metadata, model_owner_id):
        """Constructor."""

        super().__init__(all_metadata, model_owner_id)
        param_size = int(self.all_metadata[model_owner_id][0])
        self.model = self.load_model(param_size, model_owner_id)

        self.b = self.model[1]
        # TODO: Test to make sure the Array is correctly initialized
        self.W = self.model[0]

        parties = len(self.all_metadata)

        each_parties_rows = []
        total_amount_of_rows = 0
        cols = param_size - 1

        for i in list(range(model_owner_id)) + list(range(model_owner_id + 1, parties)):
            metadata = self.all_metadata[i]
            print("metadata for party {a} - {b}".format(a=i, b=metadata))
            rows = int(metadata[0])
            total_amount_of_rows += rows
            each_parties_rows.append((rows, i))

        self.data = sfix.Matrix(total_amount_of_rows, cols)

        for i in range(parties - 1):
            self.data.assign(self.load_data(cols, each_parties_rows[i][0], each_parties_rows[i][1]))

        self.data_transpose = sfix.Matrix(cols, total_amount_of_rows)

        @for_range(total_amount_of_rows)
        def _(i):
            @for_range(cols)
            def _(j):
                self.data_transpose[j][i] = self.data[i][j]

        self.labels = sint.Array(total_amount_of_rows)

        for i in range(parties - 1):
            self.labels.assign(self.load_labels(each_parties_rows[i][0], each_parties_rows[i][1]))

        # Example of how to make a field variable
        self.sample_size = total_amount_of_rows


    def load_model(self, param_size, model_owner_id):
        model_coefs = Array(param_size - 1, sfix)

        @for_range_opt(param_size - 1)
        def _(i):
            model_coefs[i] = sfix.get_input_from(model_owner_id)

        bias = sfix.get_input_from(model_owner_id)

        return (model_coefs, bias)


    def load_data(self, cols, row_length, party_id):
        data = Matrix(row_length, cols, sfix)

        @for_range_opt(row_length)
        def _(i):
            @for_range_opt(cols)
            def _(j):
                data[i][j] = sfix.get_input_from(party_id)

        return data


    def load_labels(self, row_length, party_id):
        labels = Array(row_length, sint)

        @for_range_opt(row_length)
        def _(i):
            labels[i] = sint.get_input_from(party_id)

        return labels


    def classify(self):
        """method takes a 2D list of data and classifies each row as a positive (1) or negative (0) example.
            :return a list containing the classification of each sample of data"""

        sample_size = self.sample_size
        data = self.data
        global b
        b = self.b
        W = self.W

        classifications = sint.Array(sample_size)

        threshold = 0.5  # TODO: Should be dynamic in practice

        @for_range(sample_size)
        def _(i):
            global b
            row = data[i]
            classification_intermediate = dp(W, row) + b
            classification = sig(classification_intermediate) > threshold
            classifications[i] = classification

        return classifications

    def get_true_labels(self):
        return self.labels

    def get_col(self, col):
        return self.data_transpose[int(col)]

class CNN(model):
    pass
