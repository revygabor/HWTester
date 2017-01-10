import json
from connection_hfportal import get_submissions, get_submission_file
import Utility
import os
import re

def filename_matches_filter(filename, filters):
    for filter in filters:
        match = re.match(filter, filename)
        if match:
            return True
    return False

def dirname_excluded(dirname, excludes):
    for exclude in excludes:
        if exclude in dirname:
            return True
    return False


if __name__ == "__main__":
    print("Reading plagiarism checker config file")
    with open('config_plagiarism.json') as config_file:
        config = json.load(config_file)
        hw_data = config['homeworkData']

    print("Checking jobs")
    for hw_id, hw_details in hw_data.iteritems():

        print("Checking plagiarism for: %s (%s)" % (hw_details.get("name") or hw_id, hw_id))
        for submission_data in get_submissions(hw_id, state = 7): #ertekeles lezarva
            submission_details = {}
            submission_details["id"] = submission_data[0]
            submission_details["neptun"] = submission_data[1]

            src_dir = os.path.join(config['extractDir'], hw_details.get("name") or hw_id,
                                  submission_details["neptun"], str(submission_details["id"]))

            
            data = get_submission_file(submission_details["id"])

            Utility.clean_dir(src_dir)

            try:
                Utility.unzip(data, src_dir)
            except Exception as e:
                print("extract error %s\n\n%s" % (str(e), src_dir))
            

            #find source files
            for dirName, subdirList, fileList in os.walk(src_dir):
                for fname in fileList:
                    fullfilename = os.path.join(dirName, fname)
                    if filename_matches_filter(fname, hw_details["filename filters"]) and not dirname_excluded(dirName, hw_details["ignore dirs"]):
                        print(fullfilename)
                    else:
                        os.remove(fullfilename)
