import Evaluator

class NNBinaryClassifierEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        self.details = details

    def evaluate(self, input, target_output, output, log):
        output_lines = output.split("\n")
        target_output_lines = target_output.split("\n")

        if len(output_lines) == 0:
        	return (0, "Missing line 1 in output.")
        if float(output_lines[0]) != float(target_output_lines[0]):
            return (0, "Error in line 1 in output: \n%s  \n\n expecting: %s\n\n" % (str(output_lines[0]), str(target_output_lines[0])))


        err = 0
        total = 0
        for i in range(1,len(target_output_lines)):
            if len(output_lines) <= i:
                return (0, "Missing line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))

            target_value = float(target_output_lines[i])
            try:
                value = float(output_lines[i])
            except:
                return (
                    0, "Error in line %d in output: \n%s\n\nfor input: \n%s\n" % (i + 1, log.truncate(output), input))

            if (value < 0.5) != (target_value < 0.5):
                err += 1
            total += 1
        err_rate = float(err) / float(total)

        minerr = float(self.details["min_err_rate"])
        maxerr = float(self.details["max_err_rate"])

        msgtip = ""
        if (err_rate >= 0.4):
            msgtip = "Gyozodjon meg rola, hogy a helyes mintakeszletet hasznalja: http://home.mit.bme.hu/~engedy/MI/spambase_train.csv"
            pass
        msg = "Classification error rate: %f\n\n%s" % (err_rate, msgtip)
        return (min(1.0,max(0.0,(maxerr - err_rate) / (maxerr - minerr))), msg)