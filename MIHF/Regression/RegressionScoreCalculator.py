import ScoreCalculator

class RegressionScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, details):
        self.__details = details
        pass

    def set_log(self, log):
        self.__log = log

    def score(self):
        score = 0.0
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                score += result["result"]
        

        points = int(max(0.0,min(12.0,12.0*(23.0-score)/6.0)))
        print 'RegressionScoreCalculator score:',score,'Points:',points
        return points            
    
    def message(self):
        message = []
        i = 0
        for _, results in self.__log.data["results"].iteritems():
            for result in results:
                i+=1
                message.append("%d. test result:" % i)
                message.append(result["message"])

        return "\n".join(message)