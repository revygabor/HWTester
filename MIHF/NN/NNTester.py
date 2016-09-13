import Tester
import json

class NNTester(Tester.Tester):

    def __init__(self, details):
        super(NNTester, self).__init__(details)

        tests_file = details["tests"]
        with open(tests_file, "r") as data_file:
            self.__test = json.load(data_file)
        self.__default_timeout = details.get("default timeout") or 5.0
        self.__use_with = details["use with"]

        pass


    def test(self, project_name, submission):
        (nn_details, _, extraerr) = submission.run(project_name, "")
        real_input = nn_details.strip() + "\n" + self.__test["input"]
        target_output = self.__test["target"]

        stderr = ""
        stdout = ""
        if not extraerr:
            (stdout, stderr, extraerr) = submission.run(self.__use_with, real_input,timeout = self.__default_timeout)

        if not (stderr or extraerr):
            (result, message) = self.evaluator.evaluate(real_input, target_output, stdout, submission.log)
        else:
            result = 0
            if stderr:
                message = "Runtime error:\n%s" % stderr
            else:
                message = extraerr

        submission.log.log_test(project_name, real_input, target_output, stdout, result, message)