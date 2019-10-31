import Tester
import json
import time
import numpy as np

class RecommendationSystemTester(Tester.Tester):

    def __init__(self, details):
        super(RecommendationSystemTester, self).__init__(details)

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
            print 'Testing for input', inputparams
            timeout = data.get("timeout") or self.__default_timeout
            
            pr = inputparams.split(',')
            I = int(pr[0])
            J = int(pr[1])
            missingness = float(pr[2])
            noise = float(pr[3])
            rep_dim = int(pr[4])
            
            #create target:
            
            U = np.random.rand(rep_dim,I)
            U = (U-np.mean(U,axis=0))/np.std(U,axis=0)
            V = np.random.rand(rep_dim,J)
            V = (V-np.mean(V,axis=0))/np.std(V,axis=0)

            eps = np.random.randn(I*J)*noise
            eps.shape = I,J

            R_ = np.matmul(np.transpose(U),V) + eps
            m,s = np.mean(R_),np.std(R_)

            R = np.zeros((I,J),dtype=np.int)
            for i in range(5):
                R[(R_>m-s*(i-1.5)) & (R==0)] = 5-i
            R[R==0]=1

            idx = np.random.choice(I*J,int(I*J*missingness),replace=False)
            miss = np.ones((I,J),dtype=np.int)
            miss.flat[idx] = 0

            R_miss = R*miss
            student_lines = 1
            input_for_students = "{}\t{}\t{}\n".format(int(I*J*(1.0-missingness)),I,J)
            for i in range(I):
                for j in range(J):
                    if miss[i,j]:
                        input_for_students += "{}\t{}\t{}\n".format(i,j,R[i,j])
                        student_lines += 1 
            print 'Generated tester input, student_lines = ',student_lines
            (stdout, stderr, extraerr) = submission.run(project_name, input_for_students, timeout = timeout)
            
            
            stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()

            
            eval_inputs = {}
            eval_inputs["missingness"] =  missingness
            eval_inputs["noise"] = noise
            eval_inputs["I"] = I
            eval_inputs["J"] = J
            eval_inputs["rep_dim"] = rep_dim
            eval_inputs["miss"] = miss
            eval_inputs["R"] = R


            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(eval_inputs, input_for_students, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    message = "Runtime error:\n%s\n\nfor truncated input:\n%s" % (stderr,input_for_students[:20])
                else:
                    message = 'Other Error:' + extraerr
            #result = details["score"] * result
            submission.log.log_test(project_name, eval_inputs, "", stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break
            
    