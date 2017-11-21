import Evaluator
from io import StringIO
import numpy as np

class RecommendationSystemEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
        
            hits = 5
            res = np.loadtxt(StringIO(unicode(output), "utf-8"),delimiter="\t",dtype=np.int32)
            
            R = R*(1-input['miss'])
            perf = 0
            for i in range(input['I']):
                top = set(np.argsort(-R[i,:])[:hits])
                if len(top.intersection(res[i][:hits]))>0:
                    perf += 1
            perf = (perf/float(input['I']))
            print "Performance of this evaluator:",perf
            #score = min(input["missingness"], perf)/float(input['missingness'])
            score = perf*15.0
            return (score, 'Performance = %f, required approximately %f, resulting score = %f'%(perf,input['missingness'],score))
        
        except ValueError as err:
            return (0, err.message)
        except:
            return (0, "Unknown error")

