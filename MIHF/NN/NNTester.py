import Tester
import json
import JavaSolution
import time

class NNTester(Tester.Tester):

    def __init__(self, details):
        super(NNTester, self).__init__(details)

        tests_file = details["testinputs"]
        default_timeout = details["default timeout"] or 5.0

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__default_timeout = default_timeout

        #JavaSolution.JavaSolution()
        pass


    def test(self, project_name, submission):
        pass