import ScoreCalculator


class FlappyQScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, details):
        self.__details = details
        pass

    def set_log(self, log):
        self.__log = log

    def score(self):
        score = None
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                print result["result"]
                score = result["result"]

        if (score != None and score >= 0.0):
            points = int(max(0.0, min(12.0, (score)/25.0*12.0)))
            print 'FlappyQScoreCalculator score:', score, 'Points:', points
            return points
        else:
            print 'Zero score assigned, return value of tester was', score
            return 0

    def message(self):
        message = []
        i = 0
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                i += 1
                message.append("%d. test result:" % i)
                message.append(result["message"])

        return "\n".join(message)