import Tester
import json
import time
import numpy as np
import os
import random

class RegressionTester(Tester.Tester):

    def __init__(self, details):
        super(RegressionTester, self).__init__(details)

        tests_file = details["tests"]

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__break_on_first_error = details["break on first error"]
        self.__break_on_first_wrong = details["break on first wrong"]
        self.__default_timeout = details.get("default timeout") or 5.0
        pass


    def test(self, project_name, submission):
        t0 = time.clock()
        test = self.__tests[0]
        columnorder = range(81)
        roworder_train = range(17011)
        roworder_test = range(4252)
        
        random.shuffle(columnorder)
        random.shuffle(roworder_train)
        random.shuffle(roworder_test)
        
        print 'RegressionTester: test data:',str(test), os.getcwd()
        inputs = []
        mi3_train_features = open(test["input"][0]).readlines()
        for row in roworder_train:
            line = mi3_train_features[row].strip().split('\t')
            inputs.append('\t'.join([line[c] for c in columnorder])+'\n')
        
        mi3_train_values = open(test["input"][1]).readlines()
        for row in roworder_train:
            inputs.append(mi3_train_values[row])
        
        mi3_test_features = open(test["input"][2]).readlines()
        for row in roworder_test:
            line = mi3_test_features[row].strip().split('\t')
            inputs.append('\t'.join([line[c] for c in columnorder])+'\n')
        
        mi3_test_values = open(test["target"]).readlines()
        target_output = [mi3_test_values[r] for r in roworder_test]
        
        inputstr = ''.join(inputs)
        
        print 'Time taken to shuffle inputs:',time.clock()-t0,' Input rows = %d, total len = %d target len = %d'%(len(inputs),len(inputstr),len(target_output))
        
        (stdout,stderr,extraerr) = submission.run(project_name, inputstr, timeout = self.__default_timeout)
        stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()
        
        if not (stderr or extraerr):
            (result, message) = self.evaluator.evaluate(test, target_output, stdout, submission.log)
        else:
            result = -1
            if stderr:
                if len(inputstr)> 10000:
                    message = "Runtime error:\n%s\n\n for TRUNCATED [10000 chars] input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
                else:
                    message = "Runtime error:\n%s\n\nfor complete input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
            else:
                message = extraerr +'\nstdout was:' + stdout

        submission.log.log_test(project_name, test, "", stdout, result, message)
