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
                return (0, 'Stdout did not contain the same number of lines as target output %d/%d'%(len(output),len(target_output)))
            total_error = 0.0
            for i in range(len(target_output)):
                total_error += (float(output[i]) - float(target_output[i]))**2.0
                
            RMSE = math.sqrt(total_error / float(len(target_output)))
            
            #score = int(max(0.0,min(12.0,12.0*(pctcorrect-0.6))))
            message =  'Total solution RMSE:%f'%RMSE
            print message
            return (RMSE,message)
        except ValueError as err:
            return (0, err.message)
        except Exception as e:
            print "Exception:", e.message
            return (0, "Unknown error"+e.message)

