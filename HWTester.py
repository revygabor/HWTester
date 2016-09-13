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
                submission_id = submission_data[0]
                submission_neptun = submission_data[1]
                print("Testing submission: %s (%s)" % (submission_neptun, submission_id))

                sub = Submission.Submission(submission_neptun, submission_id, hw_id, hw_details, config)
                sub.evaluate()

        print("Sleeping")
        time.sleep(60)