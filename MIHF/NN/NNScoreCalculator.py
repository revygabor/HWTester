import ScoreCalculator

class NNScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, details):
        self.__details = details
        pass

    def set_log(self, log):
        self.__log = log

    def score(self):
        totalscore = 0
        for project_name in self.__details["project_order"]:
            results = self.__log.data["results"].get(project_name)
            if not results:
                continue
            allgood = True
            for result in results:
                res = result["result"]
                if res < 1.0:
                    allgood = False
            if allgood:
                totalscore += 1
        if totalscore == 5:
            totalscore = 15
        return totalscore

    def message(self):
        message = ""
        for project_name in self.__details["project_order"]:
            results = self.__log.data["results"].get(project_name)
            message = message + "%s results:\n" % project_name
            if not results:
                message = message + "No tests run.\n\n"
                continue
            allgood = True
            for result in results:
                msg = result["message"]
                if msg:
                    message = message + msg + "\n\n"
                    allgood = False
                    break
            if allgood:
                message = message + "All tests passed.\n\n"

        return message