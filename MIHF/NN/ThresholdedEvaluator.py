import Evaluator

class ThresholdedEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        self.details = details

    def evaluate(self, input, target_output, output, log):
        output_lines = output.split("\n")
        target_output_lines = target_output.split("\n")

        dict = {}
        threshold = float(self.details["threshold"])
        for i in range(len(target_output_lines)):
            if len(output_lines) <= i:
                return (0, "Missing line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))
            values = output_lines[i].split(",")
            target_values = target_output_lines[i].split(",")
            if len(values) != len(target_values):
                return (0, "Value count mismatch in line %d in output, expecting %d values: \n%s\n\nfor input: \n%s\n" % (i + 1, len(target_values), log.truncate(output), input))
            for j in range(len(values)):
                try:
                    v = float(values[j])
                    tv = float(target_values[j])
                    sign = lambda a: (a > 0) - (a < 0)
                    ss = sign(tv)
                    minv = min(tv * (1 + threshold) + ss * threshold, tv * (1 - threshold) - ss * threshold)
                    maxv = max(tv * (1 + threshold) + ss * threshold, tv * (1 - threshold) - ss * threshold)
                    if v < minv or v > maxv:
                        return (0, "Wrong value in line %d at position %d (correct value: %f) in output: \n%s\n\nfor input: \n%s\n" % (
                        i + 1, j + 1, tv, log.truncate(output), input))
                except:
                    return (
                    0, "Error in line %d at position %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, j + 1, log.truncate(output), input))

        return (1.0, "")