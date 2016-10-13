import Evaluator
from io import StringIO
import numpy as np

class BayesMatrixFactorEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
            M = output.split('\n\n')
            U = np.loadtxt(StringIO(unicode(M[0], "utf-8")), delimiter=',')
            V = np.loadtxt(StringIO(unicode(M[1], "utf-8")), delimiter=',')

            RMSE = np.sqrt(np.mean((np.dot(U, V.T) - input["R"]) ** 2))
            ok = RMSE < input["RMSE_max"]
            score = float(ok)
            return (score, "RMSE: %f, required at most %f, accepted: %r\n" % (RMSE, input["RMSE_max"], ok))

        except ValueError as err:
            return (0, err.message)
        except:
            return (0, "Unknown error")

