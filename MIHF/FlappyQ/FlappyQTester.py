import Tester
import json
import time
import random
import importlib

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class FlappyQTester(Tester.Tester):
    def __init__(self, details):
        super(FlappyQTester, self).__init__(details)

        self.__default_timeout = details.get("default timeout") or 35.0
        pass

    def test(self, project_name, submission):
        timeout = self.__default_timeout

        input_str = ""
        target_output = ""
        (stdout, stderr, extraerr) = submission.run(project_name, input_str, timeout=timeout)

        stdout = stdout.decode('utf-8', 'ignore').encode('ascii', 'replace').strip()

        if not (stderr or extraerr):
            (result, message) = self.evaluator.evaluate(input_str, target_output, stdout, submission.log)
        else:
            result = 0
            if stderr:
                message = "Runtime error:\n%s" % (stderr.encode('utf8'))
            else:
                message = extraerr

        submission.log.log_test(project_name, input_str, target_output, stdout, result, message)

