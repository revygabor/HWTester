from connection_hfportal import get_submission_file, post_result
import Utility
import Log
import os

class Submission(object):
    def __init__(self, submission_details, hw_id, hw_details, config):

        self.WORKING_DIR = config['workingDir']
        self.EXTRACT_DIR = config['extractDir']
        self.LOG_DIR = config['logDir']
        self.CORRECTOR_NAME = config['appName']
        self.MESSAGE_MAX_LENGTH = config['messageMaxLength']
        self.log_to_html = config['logToHTML']
        self.enable_write_to_database = config['enableWriteToDatabase']

        self.submission_details = submission_details
        self.hw_id = hw_id
        self.hw_details = hw_details

        self.projectsolutions = {}

        self.log = None


    def evaluate(self):
        data = get_submission_file(self.submission_details["id"]) #returns the zip file
        self.log = Log.Log(self.submission_details, self.hw_id, self.hw_details.get("name") or self.hw_id, self.MESSAGE_MAX_LENGTH)

        src_dir = os.path.join(self.EXTRACT_DIR, str(self.hw_id), self.submission_details["neptun"], str(self.submission_details["id"]))
        #creates a directory like /media/50gb/src/[233 or OPRE HF1]/TEST03/7000/
        Utility.clean_dir(src_dir)
        Utility.clean_dir(self.WORKING_DIR)

        try:
            Utility.unzip(data, src_dir)
        except Exception as e:
            self.log.log_error("compile error", str(e))

        scorecalculator = None
        if not self.log.has_error("compile error"):
            scorecalculator = Utility.get_class(self.hw_details.get("score calculator"))(
                self.hw_details.get("score calculator details"))

            self.log.log_start_time()
            solution_for_type = {}
            if self.hw_details.get("projects") == None:
                self.log.log_error("hw_details.get returned nonetype",str(self.hw_details))
                print "hw_details.get returned nonetype", str(self.hw_details)
                return
            for project_name, project_details in self.hw_details.get("projects").iteritems():
                solution_type = project_details.get("solution type")
                if solution_type in solution_for_type:
                    self.projectsolutions[project_name] = solution_for_type[solution_type]
                    continue

                solution = Utility.get_class(solution_type)(src_dir, self.WORKING_DIR, self.hw_details.get('firejail profile'))
                solution_for_type[solution_type] = solution
                self.projectsolutions[project_name] = solution

                (stdout, stderr) = solution.prepare()
                if stderr:
                    self.log.log_error("compile error", stderr)

            for project_name, project_details in self.hw_details.get("projects").iteritems():
                tester = Utility.get_class(project_details.get("tester"))(project_details.get("tester details"))
                tester.test(project_name, self)

            self.log.log_finish_time()
            scorecalculator.set_log(self.log)

        if self.enable_write_to_database:
            if self.log.has_error():
                post_result(self.submission_details["id"], self.CORRECTOR_NAME, 9, 0, self.log.message())
            else:
                post_result(self.submission_details["id"], self.CORRECTOR_NAME, 7,
                            scorecalculator.score(),
                            scorecalculator.message(),scorecalculator.getimscpoint())
        if self.log_to_html:
            self.log.log2html(self.LOG_DIR, scorecalculator)

    def run(self, project_name, input, timeout=5.0):
        solution = self.projectsolutions[project_name]
        (runnable, extraerr) = solution.find_runnable(project_name)
        if extraerr or not runnable:
            return ("", "", extraerr)
        else:
            return solution.run(runnable, input, timeout)

    def is_personal(self):
        return "personal_index" in self.submission_details

    def personal_index(self):
        return int(self.submission_details.get("personal_index"))