import ScoreCalculator

class SimpleScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, params):
        self.__details = params

    def set_log(self, log):
        self.__log = log

    def score(self):
        totalscore = 0
        for i in range(len(self.__details["project_order"])):
            project_name = self.__details["project_order"][i]
            score = int(self.__details["scores"][i])
            results = self.__log.data["results"].get(project_name)
            if not results:
                continue
            all_good = True
            for result in results:
                res = result["result"]
                if res < 1.0:
                    all_good = False
            if all_good:
                totalscore += score

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
                message = message + "OK.\n\n"

        return message