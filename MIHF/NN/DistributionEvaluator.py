import Evaluator
import numpy as np
import scipy.stats as stats

class DistributionEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        self.details = details
        pass

    def evaluate(self, input, target_output, output, log):
        output_lines = output.split("\n")
        target_output_lines = target_output.split("\n")

        dict = {}
        for i in range(len(target_output_lines)):
            if len(output_lines) <= i:
                return (0, "Missing line %d in output: \n%s\n\nfor input: \n%s\n" % (i+1, log.truncate(output), input))
            values = output_lines[i].split(",")
            target_values = target_output_lines[i].split(",")
            if len(values) != len(target_values):
                return (0, "Error in line %d in output: \n%s\n\nfor input: \n%s\n" % (i+1, log.truncate(output), input))
            for j in range(len(values)):
                if target_values[j] in self.details:
                    if target_values[j] not in dict:
                        dict[target_values[j]] = []
                    dict[target_values[j]].append(values[j])
                else:
                    if float(values[j]) != float(target_values[j]):
                        return (0, "Error in line %d at value %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, j+1, log.truncate(output), input))

        for k, v in dict.iteritems():
            dist = self.details[k]
            if dist["distribution"] != "normal":
                return (0, "not implemented distribution type")
            mean = dist["mean"]
            std = dist["std"]
            confidence = dist["confidence"]

            x = (np.array(v)).astype(np.float)
            x = (x - mean) / std

            (k,p) = stats.kstest(x,'norm')

            if p < 1-confidence:
                return (0, "Wrong distribution of values in output: \n%s\n\nfor input: \n%s\n" % (log.truncate(output), input))

        return (1.0, "")
