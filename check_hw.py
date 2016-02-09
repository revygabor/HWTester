import json
from connection_hfportal import get_new_submissions, get_submission_file, post_result
from prepare_hw import unzip, java_compile, run_firejail_java, java_compile_all, clean_dir


with open('config.json') as config_file:  
    config = json.load(config_file)
    hw_data = config['homeworkData']
    WORKING_DIR = config['workingDir']
    CORRECTOR_NAME = config['appName']
    MESSAGE_MAX_LENGTH = config['messageMaxLength']

def truncate(s):
    if len(s) > MESSAGE_MAX_LENGTH:
        return "[...]%s" % s[-MESSAGE_MAX_LENGTH:]
    else:
        return s

def bad_output_message(output, input):
    return "Bad output '%s' for input '%s'." % (truncate(output), input)


for hw_id, hw_details in hw_data.iteritems():
    for submission_id in get_new_submissions(hw_id):
        print(submission_id)
        data = get_submission_file(submission_id)
        
        try:
            unzip(data, WORKING_DIR)
        except Exception as e:
            post_result(submission_id, CORRECTOR_NAME, 9, 0, truncate(e))
            break

        (stdout, stderr) = java_compile_all(WORKING_DIR)
        if stderr:
            post_result(submission_id, CORRECTOR_NAME, 9, 0, truncate(stderr))
            break

        for input,target_output in hw_details['testcases'].iteritems():
            (stdout, stderr) = run_firejail_java(hw_details['classname'],input,hw_details['firejail profile'])
            stdout = stdout.strip()
            target_output = target_output.strip()
            if stdout != target_output or stderr:                
                break            

        if stderr:
            post_result(submission_id, CORRECTOR_NAME, 9, 0, truncate(stderr))
            break
        if stdout != target_output:
            post_result(submission_id, CORRECTOR_NAME, 7, 0, bad_output_message(stdout, input))
            break

        post_result(submission_id, CORRECTOR_NAME, 7, hw_details['fullscore'], "Passed all tests.")

