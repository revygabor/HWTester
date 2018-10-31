import Evaluator
from io import StringIO

class SentimentAnalysisEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
            output = output.split('\n')
            if len(output) != len(target_output):
                return (0, 'Stdout did not contain the same number of lines as target output %d/%d'%(len(output),len(target_output)))
            total = 0
            correct = 0
            for i in range(len(target_output)):
                total += 1
                if int(output[i]) == int(target_output[i]):
                    correct+=1
            pctcorrect = float(correct)/float(total)
            #score = int(max(0.0,min(12.0,12.0*(pctcorrect-0.6))))
            return (pctcorrect, 'Fraction of correct labels:%f'%pctcorrect)
        except ValueError as err:
            return (0, err.message)
        except Exception as e:
            print "Exception:", e.message
            return (0, "Unknown error"+e.message)

