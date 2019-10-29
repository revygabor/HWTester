import ScoreCalculator

class SimpleTestBasedScoreCalculator(ScoreCalculator.ScoreCalculator):

    def __init__(self, params):
        self.__details = params

    def set_log(self, log):
        self.__log = log

    def score(self):
        totalscore = 0
        score = int(self.__details["scores_per_test"])
        for i in range(len(self.__details["project_order"])):
            project_name = self.__details["project_order"][i]
            results = self.__log.data["results"].get(project_name)
            #print "results for test", results, project_name, score
            if not results:
                continue
            for result in results:
                print 'result=',result["result"]
                res = result["result"]
                totalscore += res * score
        if 'max_score' in self.__details:
            totalscore = min(self.__details['max_score'],totalscore)
        print 'Total score = ', totalscore
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
