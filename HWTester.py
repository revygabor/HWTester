import json
import os
import time
from connection_hfportal import get_submissions, get_submission_file, post_result
import Utility
import importlib
import Log

if __name__ == "__main__":
    while True:
        print("Reading config file")
        with open('config.json') as config_file:
            config = json.load(config_file)
            hw_data = config['homeworkData']
            WORKING_DIR = config['workingDir']
            EXTRACT_DIR = config['extractDir']
            LOG_DIR = config['logDir']
            CORRECTOR_NAME = config['appName']
            MESSAGE_MAX_LENGTH = config['messageMaxLength']
            break_on_first_error = config['breakOnFirstError']
            log_to_html = config['logToHTML']
            enable_write_to_database = config['enableWriteToDatabase']
            if 'stop' in config:
                break

        print("Checking jobs")
        for hw_id, hw_details in hw_data.iteritems():
            print("Checking submissions for: %s (%s)" % (hw_details.get("name") or hw_id, hw_id))
            for submission_data in get_submissions(hw_id):
                submission_id = submission_data[0]
                submission_neptun = submission_data[1]
                print("Testing submission: %s (%s)" % (submission_neptun, submission_id))

                log = Log.Log(submission_neptun, submission_id, hw_id, hw_details.get("name") or hw_id, MESSAGE_MAX_LENGTH)

                data = get_submission_file(submission_id)

                src_dir = os.path.join(EXTRACT_DIR, hw_details.get("name") or hw_id, submission_neptun, str(submission_id))

                Utility.clean_dir(src_dir)
                Utility.clean_dir(WORKING_DIR)

                try:
                    Utility.unzip(data, src_dir)
                except Exception as e:
                    log.log_error("compile error", str(e))

                if not log.has_error("compile error"):
                    scorecalculatormod = importlib.import_module(hw_details.get("score calculator"))
                    scorecalculatorclass = getattr(scorecalculatormod, hw_details.get("score calculator"))
                    scorecalculator = scorecalculatorclass(hw_details.get("score calculator details"))

                    log.log_start_time()
                    for project_name, project_details in hw_details.get("runnables").iteritems():
                        for solution_type in project_details.get("allowed solution"):
                            solutionmod = importlib.import_module(solution_type)
                            solutionclass = getattr(solutionmod, solution_type)
                            solution = solutionclass(src_dir, WORKING_DIR, hw_details.get('firejail profile'))


                            (stdout, stderr) = solution.prepare()
                            if stderr:
                                log.log_error("compile error", stderr)
                            else:
                                break


                        testermod = importlib.import_module(project_details.get("tester"))
                        testerclass = getattr(testermod, project_details.get("tester"))
                        tester = testerclass(project_details.get("tester details"))

                        runnable = solution.find_runnable(project_name)
                        tester.test(runnable, project_name, solution, log)
                    log.log_finish_time()


                    if enable_write_to_database:

                        if log.has_error():
                            post_result(submission_id, CORRECTOR_NAME, 9, 0, log.message())
                        else:
                            post_result(submission_id, CORRECTOR_NAME, 7,
                                        scorecalculator.score(log),
                                        log.message())
                    if log_to_html:
                        log.log2html(LOG_DIR, scorecalculator)
                else:
                    if enable_write_to_database:
                        post_result(submission_id, CORRECTOR_NAME, 9, 0, log.message())
                    if log_to_html:
                        log.log2html(LOG_DIR, None)


        print("Sleeping")
        time.sleep(60)