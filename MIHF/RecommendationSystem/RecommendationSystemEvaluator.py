import Evaluator
from io import StringIO
import numpy as np
import traceback
import sys

class RecommendationSystemEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
        
            print 'Started RecommendationSystemEvaluator, output recieved: %s , total number of chars recieved = %d'%(output[0:min(len(output),50)],len(output))
            hits = 5
            #striofile = StringIO(unicode(output), "utf-8")
            
            striofile = StringIO(unicode(output), newline = u'\n')
            print 'Striofile created succesfully'
            res = np.loadtxt(striofile,delimiter="\t",dtype=np.int32)
            print 'If you can read this then text loaded correctly, dimensions of striofile:',res.shape
            R = input['R']*(1-input['miss'])
            perf = 0
            for i in range(input['I']):
                top = set(np.argsort(-R[i,:])[:hits])
                if len(top.intersection(res[i][:hits]))>0:
                    perf += 1
            perf = (perf/float(input['I']))
            print "Performance of this evaluator:",perf
            #score = min(input["missingness"], perf)/float(input['missingness'])
            score = perf/float(input['missingness'])
            return (score, 'Performance = %f, required approximately %f, resulting score = %f'%(perf,input['missingness'],score))
        
        except ValueError as err:
            print err.message
            print (err)
            traceback.print_exc()

            #raise err
            return (0, 'ValueError during the parsing of the user output, error was: %s \n%s \n The first 200 characers of the user output was:\n %s \n The last 200 characters were:\n %s'%(err.message ,str(err), unicode(output)[:200],unicode(output)[-200:]))
        except IndexError as err:
            print err.message
            print (err)
            traceback.print_exc()
            return (0,'The dimensions of the user output was %s, make sure these match the specifications!\n %s \n Make SURE that your output is formatted correctly!\nThe first 200 characers of the user output was:\n %s \n The last 200 characters were:\n %s' %(res.shape,err.message,  unicode(output)[:200],unicode(output)[-200:]))
        except:
            print ("other, unspecified parsing error:",str(sys.exc_info()[0]))
            return (0, "Unknown error: for user output of %s "%(unicode(output)))

