from Compiler.types import *
from Compiler.library import *


class metric():
    """ Class defines multiple metrics for determining fairness
    :param actual_labels: Actual labels of the data
    :param predicted_labels: Predicted labels of the data
    """

    def __init__(self, actual_labels, predicted_labels, protected_col, protected_col_vals,
                 debug=False, report_loss=None):
        self.actual_labels = actual_labels
        self.predicted_labels = predicted_labels
        self.protected_col = protected_col
        self.protected_col_vals = protected_col_vals

    def traditional_metrics(self):
        """ Calculates some of the most common metrics:
            True Positive (TP)
            False Positive (FP)
            True Negative (TN)
            False Negative (FN)

            Calculating TP gives us FP nearly for free. Likewise, TN and FN have have the same relationship. This,
            and the fact that it takes the same communication/local complexity to calculate all at once,
            makes it advantageous to calculate all values in one call.

            input actual_labels: The shares of the actual labels of data
            input predicted_labels: The shares of the predicted labels of data

            returns (TP, FP, TN, FN) """

        protected_col = self.protected_col
        protected_col_vals = self.protected_col_vals

        actual_labels = self.actual_labels
        predicted_labels = self.predicted_labels

        l = len(actual_labels)

        assert (l == len(predicted_labels))
        assert (l == len(protected_col))

        # TODO: Needs to be more general actually... need to have as many arrays as there are attribute values
        # TP, FP, TN, FN
        male = sint.Array(4)
        female = sint.Array(4)

        @for_range(4)
        def _(i):
            male[i] = sint(0)
            female[i] = sint(0)

        @for_range_opt(l)
        def _(i):
            a = predicted_labels[i]
            b = actual_labels[i]

            x = (a == 1)
            y = (b == 1)
            z = 1 - x
            w = 1 - y

            is_male = (protected_col[i] == protected_col_vals[0])
            is_female = 1 - is_male

            male[0] += (z * w) * is_male
            male[1] += (z * b) * is_male
            male[2] += (x * w) * is_male
            male[3] += (x * y) * is_male

            female[0] += (z * w) * is_female
            female[1] += (z * b) * is_female
            female[2] += (x * w) * is_female
            female[3] += (x * y) * is_female

        return male, female


    def equalized_odds(self):
        male, female = self.traditional_metrics()

        # male = maleSecret.reveal_nested()
        # female = femaleSecret.reveal_nested()

        # male_res = male[1].int_div(male[1] + male[2])
        # fem_res = female[1].int_div(female[1] + female[2])

        return male, female


