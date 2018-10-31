import Tester
import json
import time
import numpy as np
import os

class SentimentAnalysisTester(Tester.Tester):

    def __init__(self, details):
        super(SentimentAnalysisTester, self).__init__(details)

        tests_file = details["tests"]

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__break_on_first_error = details["break on first error"]
        self.__break_on_first_wrong = details["break on first wrong"]
        self.__default_timeout = details.get("default timeout") or 5.0
        pass


    def test(self, project_name, submission):
        
        test = self.__tests[0]
        print 'SentimentAnalysisTester: test data:',str(test), os.getcwd()
        inputs = []
        inputs += open(test["input"][0]).readlines()
        inputs += open(test["input"][1]).readlines()
        inputs += open(test["input"][2]).readlines()
        #print 'SentimentAnalysisTester: input size is:', len(inputs)
        inputstr = ''.join(inputs)
        target_output = open(test["target"]).readlines()
        
        
        (stdout,stderr,extraerr) = submission.run(project_name, inputstr, timeout = self.__default_timeout)
        stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()
        
        if not (stderr or extraerr):
            (result, message) = self.evaluator.evaluate(test, target_output, stdout, submission.log)
        else:
            result = 0
            if stderr:
                if len(inputstr)> 10000:
                    message = "Runtime error:\n%s\n\n for TRUNCATED [10000 chars] input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
                else:
                    message = "Runtime error:\n%s\n\nfor complete input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
            else:
                message = extraerr +'\nstdout was:' + stdout

        submission.log.log_test(project_name, test, "", stdout, result, message)
