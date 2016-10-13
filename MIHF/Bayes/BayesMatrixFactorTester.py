import Tester
import json
import time
import numpy as np

class BayesMatrixFactorTester(Tester.Tester):

    def __init__(self, details):
        super(BayesMatrixFactorTester, self).__init__(details)

        tests_file = details["tests"]

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__break_on_first_error = details["break on first error"]
        self.__break_on_first_wrong = details["break on first wrong"]
        self.__default_timeout = details.get("default timeout") or 5.0
        pass


    def test(self, project_name, submission):

        tests = self.__tests

        for data in tests:
            timeout = self.__default_timeout

            inputparams = data["input"]
            timeout = data.get("timeout") or self.__default_timeout

            pr = inputparams.split(",")

            I = int(pr[0])
            J = int(pr[1])
            L = int(pr[2])
            beta = float(pr[3])
            RMSE_max = float(pr[4])

            # Create target matrix
            R = np.random.rand(I, J)

            input = '{0},{1},{2},{3:.1f}\n'.format(I, J, L, beta)
            input_first_row = input
            input += '\n'.join([','.join(['{0:.3f}'.format(j) for j in R[i, :]]) for i in range(I)])


            (stdout, stderr, extraerr) = submission.run(project_name, input, timeout = timeout)

            stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()

            eval_inputs = {}
            eval_inputs["R"] = R
            eval_inputs["RMSE_max"] = RMSE_max
            eval_inputs["I"] = I
            eval_inputs["J"] = J
            eval_inputs["L"] = L
            eval_inputs["beta"] = beta


            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(eval_inputs, None, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    message = "Runtime error:\n%s\n\nfor input:\n%s" % (stderr,input_first_row)
                else:
                    message = extraerr

            submission.log.log_test(project_name, eval_inputs, "", stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break