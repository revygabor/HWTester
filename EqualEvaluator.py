import Evaluator

class EqualEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        if output != target_output:
            return (0.0, "Wrong answer in output: \n%s\n\nfor input: \n%s\n" % (log.truncate(output), input))

        return (1.0, "")
