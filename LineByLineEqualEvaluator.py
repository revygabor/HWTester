import Evaluator

class LineByLineEqualEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        if output != target_output:
            output_lines = output.split("\n")
            target_output_lines = target_output.split("\n")

            goodlines = 0
            errmsg = None
            for i in range(len(target_output_lines)):
                if len(output_lines) <= i:
                    if errmsg:
                        return (float(goodlines) / len(target_output_lines), errmsg)
                    return (float(goodlines) / len(target_output_lines), "Missing line %d in output: \n%s\n\nfor input: \n%s\n" % (i+1, log.truncate(output), input))
                if output_lines[i].strip() != target_output_lines[i].strip() and not errmsg:
                    errmsg = "Wrong answer in line %d of output: \n%s\n\nfor input: \n%s\n" % (i+1, log.truncate(output), input)
                if output_lines[i].strip() == target_output_lines[i].strip():
                    goodlines += 1
                    #print 'goodlines +=1',output_lines[i],target_output_lines[i]
            return (float(goodlines) / len(target_output_lines), errmsg)

        return (1.0, "")
