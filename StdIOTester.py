import Tester
import json
import time

class StdIOTester(Tester.Tester):

    def __init__(self, details):
        super(StdIOTester, self).__init__(details)

        tests_file = details["tests"]
        default_timeout = details["default timeout"] or 5.0
        break_on_first_error = details["break on first error"]
        break_on_first_wrong = details["break on first wrong"]

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__break_on_first_error = break_on_first_error
        self.__break_on_first_wrong = break_on_first_wrong
        self.__default_timeout = default_timeout
        pass


    def test(self, project_name, submission):
        for data in self.__tests:
            timeout = self.__default_timeout
            if isinstance(data, dict):
                input = data["input"]
                target_output = data["target"]
                timeout = data.get("timeout") or self.__default_timeout
            elif isinstance(data, list):
                input = data[0]
                target_output = data[1]

            (stdout, stderr, extraerr) = submission.run(project_name, input, timeout = timeout)

            stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()
            target_output = target_output.strip()


            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(input, target_output, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    message = "Runtime error:\n%s" % stderr
                else:
                    message = extraerr

            submission.log.log_test(project_name, input, target_output, stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break