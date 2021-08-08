class model():

    def __init__(self, layers):
        self.layers = layers

        # TODO: Figure out the best way to implement the layers

    # Reads model params into a tensor
    def read(self, raw_model):
        pass

    # Classify data
    def classify(self, data):
        pass


class logistic_regression(model):
    """ Class that allows us to read, and classify with a logistic regression model."""

    def __init__(self):
        """Constructor."""
        # Example of how to make a field variable
        self.a_field_variable = 0

        # Example of how to call parents constructor (you don't have to use it if you don't feel a need for it)
        super().__init__(0)

    # (Note) This will have to later be replaced with MP-SPDZ friendly code (one reason it is unfriendly is that is
    # that we can't have x in the denominator - this has to do with how our encrypted shares of data 'live' in a
    # mathematical ring. Values in a ring may not have an multiplicative inverse). For now, this will do just fine
    # though.
    def sigmoid(self, x):
        return 1 / (1 + 2.71 ** (-x))

    # (Note) You can can decide how the list 'raw_model' should be formatted. For example, it could be of the form
    # [bias, [weight_1, weight_2, ..., weight_n]]. You just have to read it here, and save it somehow to this instance
    # of the class. So for example, you could save the bias in a field variable as 'self.bias = bias'. The weights and
    # bias should be used in the classify method to classify data
    def read(self, raw_model):
        """Takes a list of model parameters and breaks them up into weights and a bias
                    :param raw_model: parameters of the LR model"""
        pass

    # (Note) To classify, we take a sample (row) of data, and perform sigmoid(dot_product(weights, sample) + bias) > 0.5
    # If the comparison result is true, we return a class label of 1. If it is false, we return a class label of 0.
    def classify(self, data):
        """method takes a 2D list of data and classifies each row as a positive (1) or negative (0) example.
            :param data: Data to classify
            :return a list containing the classification of each sample of data"""
        pass


class CNN(model):
    pass
