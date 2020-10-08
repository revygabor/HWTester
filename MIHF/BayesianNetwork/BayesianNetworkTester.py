import Tester
import json
import time
import random
import importlib
from MIHF.BayesianNetwork.test_generator import generate_task

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BayesianNetworkTester(Tester.Tester):
    def __init__(self, details):
        super(BayesianNetworkTester, self).__init__(details)

        tests_file = details["tests"]

        with open(tests_file, "r") as data_file:
            self.__test_parameters = json.load(data_file)
        self.__break_on_first_error = details["break on first error"]
        self.__break_on_first_wrong = details["break on first wrong"]
        self.__default_timeout = details.get("default timeout") or 5.0
        pass

    def test(self, project_name, submission):
        for params in self.__test_parameters:
            timeout = self.__default_timeout

            try:
                input_str, target_output = generate_task(params)
            except:
                input_str = ""
                target_output = ""
                print >> sys.stderr, "Unexpected error: " + str(sys.exc_info()[0])

            if input_str:
                (stdout, stderr, extraerr) = submission.run(project_name, input_str, timeout = timeout)
            else:
                stdout = ""
                stderr = ""
                extraerr = "Internal error. If this issue persists," \
                           "please contact the lecturer, or the homework support team."

            stdout = stdout.decode('utf-8', 'ignore').encode('ascii', 'replace').strip()

            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(input_str, target_output, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    message = "Runtime error:\n%s\n\nfor input:\n%s" % (stderr.encode('utf8'), input_str.encode('utf8'))
                else:
                    message = extraerr

            submission.log.log_test(project_name, input_str, target_output, stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break
