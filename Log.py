import time
import os

class Log(object):

    def __init__(self, neptun, id, hwid, hw_name, max_len):
        self.data = {}
        self.data["neptun"] = neptun
        self.data["id"] = id
        self.data["hwid"] = hwid
        self.data["hw_name"] = hw_name
        self.data["errors"] = {}
        self.data["results"] = {}
        self.__max_len = max_len

    def truncate(self, s):
        if len(s) > self.__max_len:
            return "[...]%s" % s[-self.__max_len:]
        else:
            return s

    def log_test(self, project_name, input, target_output, stdout, result, message):
        if project_name not in self.data["results"]:
            self.data["results"][project_name] = []
        self.data["results"][project_name].append({'input': input, 'target_output': target_output, 'output': stdout, 'result': result, 'message': message})


    def log_error(self, error, message):
        self.data["errors"][error] = message

    def has_error(self, error=None):
        if not error:
            return bool(self.data["errors"])
        else:
            return error in self.data["errors"]

    def log_start_time(self):
        self.data["start"] = time.clock()

    def log_finish_time(self):
        self.data["end"] = time.clock()

    def message(self):
        if "compile error" in self.data["errors"]:
            return "COMPILE ERROR: %s \n" % (self.truncate(self.data["errors"]["compile error"]))
        else:
            for k, v in self.data["errors"].iteritems():
                return "ERROR: %s \n" % (self.truncate(v))
        return ""

    def log2html(self, log_dir, score_calculator):
        path = os.path.join(log_dir, self.data["hw_name"], self.data["neptun"])
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, "log_%s.html" % self.data["id"]), "w") as file:
            file.write("<body>\n")
            file.write("<b>ID:</b> %s <br>\n" % (self.data["id"]))
            file.write("<b>HW ID:</b> %s <br>\n" % (self.data["hwid"]))
            file.write("<b>NEPTUN:</b> %s <br>\n" % (self.data["neptun"]))

            if "compile error" in self.data["errors"]:
                file.write("<b>COMPILE ERROR:</b> %s <br>\n" % (self.data["errors"]["compile error"]))
            else:
                #file.write("<b>GOOD RATIO:</b> %d/%d <br>" % (self.data["good"], len(self.data["result"])))
                #file.write("<b>SCORE:</b> %d <br>" % (score_from_log(log, scorelimits)))     score_calculator
                file.write("<b>TEST DURATION:</b> %f s<br>\n" % (self.data["end"] - self.data["start"]))


                for classname, resultdata in self.data["results"].iteritems():
                    file.write("<br><br><b>MAIN CLASS:</b> %s <br>\n" % (classname))
                    file.write('<table border="1">\n')
                    file.write("<tr>\n")
                    file.write("<th>INPUT</th><th>TARGET_OUTPUT</th><th>OUTPUT</th><th>RESULT</th><th>MESSAGE</th>\n")
                    file.write("</tr>\n")
                    for row in resultdata:
                        file.write("<tr>\n")
                        file.write("<td>")
                        file.write(row['input'].replace("\n", "<br>"))
                        file.write("</td>\n")
                        file.write("<td>")
                        file.write(row['target_output'].replace("\n", "<br>"))
                        file.write("</td>\n")
                        file.write("<td>")
                        file.write(row['output'].replace("\n", "<br>"))
                        file.write("</td>\n")
                        file.write("<td>")
                        file.write(str(row['result']))
                        file.write("</td>\n")
                        file.write("<td>")
                        file.write(row['message'].replace("\n", "<br>"))
                        file.write("</td>\n")
                        file.write("</tr>\n")
                    file.write("</table>")
            if score_calculator:
                file.write("<br><br><b>SCORE TO HF PORTAL:</b> %s <br>\n" % (str(score_calculator.score())))
                file.write("<b>MESSAGE TO HF PORTAL:</b><br>\n%s <br>\n" % (score_calculator.message()))
            file.write("</body>\n")
        pass