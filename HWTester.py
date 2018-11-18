import json
import time
from connection_hfportal import get_submissions
import Submission

if __name__ == "__main__":
    while True:
        print("Reading config file")
        with open('config.json') as config_file:
            config = json.load(config_file)
            hw_data = config['homeworkData']
            if 'stop' in config:
                break

        print("Checking jobs")
        for hw_id, hw_details in hw_data.iteritems():
            print("Checking submissions for: %s (%s)" % (hw_details.get("name") or hw_id, hw_id))
            for submission_data in get_submissions(hw_id):
                submission_details = {}
                submission_details["id"] = submission_data[0]
                submission_details["neptun"] = submission_data[1]
                if config['isDebug']:
                    if not submission_details["neptun"].startswith("TEST"):
                        continue
                personal = ""
                if (len(submission_data) > 2):
                    submission_details["personal_index"] = submission_data[2]
                    personal = "pid: %s" % submission_details["personal_index"]

                print("Testing submission: %s (%s) %s"% (submission_details["neptun"], submission_details["id"], personal, ))
                #print("Testing submission: %s (%s) %s %s" % (submission_details["neptun"], submission_details["id"], personal, str(hw_details)))

                sub = Submission.Submission(submission_details, hw_id, hw_details, config)
                sub.evaluate()

        print "Sleeping", time.clock()
        time.sleep(10)
