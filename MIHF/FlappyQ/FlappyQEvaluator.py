import Evaluator
import sys


class FlappyQEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input_str, target_output, output, log):
        try:
            if not output:
                raise ValueError("Received no result. This could be caused by the execution "
                                 "exceeding the given time limit.")
            output_lines = output.strip().split('\n')
            if len(output_lines) > 1:
                raise ValueError("Unexpected output. No need for your program to have an output.")

            output_value = int(output_lines[-1])
            return (output_value, "")

        except (ValueError, OverflowError, TypeError) as err:
            return (0, err.message)
        except:
            print sys.exc_info()[0]
            return (0, "Unknown error:\n {0}".format(sys.exc_info()[0]))
