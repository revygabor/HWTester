import Evaluator

class ThresholdedEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        self.details = details

    def evaluate(self, input, target_output, output, error, log):
        if error:
            return (0.0, "Runtime error:\n%s\n" % error)

        output_lines = output.split("\n")
        target_output_lines = target_output.split("\n")

        dict = {}
        treshold = float(self.details["threshold"])
        for i in range(len(target_output_lines)):
            if len(output_lines) <= i:
                return (0, "Missing line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))
            values = output_lines[i].split(",")
            target_values = target_output_lines[i].split(",")
            if len(values) != len(target_values):
                return (0, "Error in line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))
            for j in range(len(values)):
                try:
                    if float(values[j]) > float(target_values[j]) * (1 + treshold) or float(values[j]) < float(target_values[j]) * (1 - treshold):
                        return (0, "Error in line %d at value %d in output: \n%s\n\nfor input: \n%s\n" % (
                        i + 1, j + 1, log.truncate(output), input))
                except:
                    return (
                    0, "Error in line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))



        return (1.0, "")