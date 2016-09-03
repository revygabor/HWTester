import importlib

class Tester(object):
    def __init__(self, details):
        evaluatormod = importlib.import_module(details["evaluator"])
        evaluatorclass = getattr(evaluatormod, details["evaluator"])
        self.evaluator = evaluatorclass(details["evaluator details"])

    def test(self, runnable, project_name, solution, log):
        raise NotImplementedError("not implemented")
