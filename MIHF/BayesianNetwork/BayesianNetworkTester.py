import Tester
import json
import time
import random
import importlib
from test_generator import generate_task

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
            input_str, target_output = generate_task(params)

            (stdout, stderr, extraerr) = submission.run(project_name, input_str, timeout = timeout)

            stdout = stdout.decode('utf-8', 'ignore').encode('ascii', 'replace').strip()

            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(input_str, target_output, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    # name = school_name.encode('utf8')
                    message = "Runtime error:\n%s\n\nfor input:\n%s" % (stderr.encode('utf8'), input.encode('utf8'))
                else:
                    message = extraerr

            submission.log.log_test(project_name, input, target_output, stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break