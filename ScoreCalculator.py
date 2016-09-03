class ScoreCalculator(object):

    def __init__(self, params):
        pass

    def set_log(self, log):
        self.__log = log

    def score(self):
        raise NotImplementedError("not implemented")

    def message(self):
        raise NotImplementedError("not implemented")