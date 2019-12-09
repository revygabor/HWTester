import Evaluator
from io import StringIO
import math

class RegressionEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
            output = output.split('\n')
            if len(output) != len(target_output):
                return (-1, 'Stdout did not contain the same number of lines as target output (%d user lines/%d target lines)'%(len(output),len(target_output)))
            total_error = 0.0
            current_line = ""
            for i in range(len(target_output)):
                current_line = output[i]
                total_error += (float(output[i]) - float(target_output[i]))**2.0
                
            RMSE = math.sqrt(total_error / float(len(target_output)))
            
            #score = int(max(0.0,min(12.0,12.0*(pctcorrect-0.6))))
            message =  'Total solution RMSE:%f'%RMSE
            print message
            return (RMSE,message)
        except ValueError as err:
            return (-1, str(err.message) + "\nCurrent line:\n"+current_line)
        except Exception as e:
            print "Exception:", e.message
            return (-1, "Unknown error"+str(e.message) + "\nCurrent line:\n"+current_line)

