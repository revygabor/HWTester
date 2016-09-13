import Utility

class Tester(object):
    def __init__(self, details):
        self.evaluator = Utility.get_class(details["evaluator"])(details["evaluator details"])

    def test(self, project_name, submission):
        raise NotImplementedError("not implemented")
