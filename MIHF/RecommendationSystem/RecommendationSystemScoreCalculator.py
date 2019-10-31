import ScoreCalculator

class RecommendationSystemScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, details):
        self.__details = details
        pass

    def set_log(self, log):
        self.__log = log

    def score(self):
        test_count = 0
        summed_score = 0
        #print 'Scoring', self.__details["score"]
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                #print 'Scoring...',result["result"]
                test_count += 1
                summed_score += result["result"]

        print 'Scored, test_count=',test_count,'summed_score = ',summed_score
        if test_count > 0:
            return int(max(0, min(self.__details["score"],self.__details["score"]*(summed_score/float(test_count)))))
        else:
            return 0

    def message(self):
        message = []
        i = 0
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                i+=1
                message.append("%d. test result:" % i)
                message.append(result["message"])

        return "\n".join(message)