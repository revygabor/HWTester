import json
import shutil
import os
import time
from connection_hfportal import get_new_submissions, get_submission_file, post_result
from prepare_hw import unzip, java_compile, run_firejail_java, java_compile_all, clean_dir, find_java_class_with_package


with open('config.json') as config_file:  
    config = json.load(config_file)
    hw_data = config['homeworkData']
    WORKING_DIR = config['workingDir']
    EXTRACT_DIR = config['extractDirPrefix']    
    CORRECTOR_NAME = config['appName']
    MESSAGE_MAX_LENGTH = config['messageMaxLength']
    break_on_first_error = config['breakOnFirstError']
    break_on_first_timeout = config['breakOnFirstTimeout']
    log_to_html = config['logToHTML']
    enable_write_to_database = config['enableWriteToDatabase']


def truncate(s):
    if len(s) > MESSAGE_MAX_LENGTH:
        return "[...]%s" % s[-MESSAGE_MAX_LENGTH:]
    else:
        return s

def bad_output_message(output, input):
    return "Bad output '%s' for input '%s'." % (truncate(output), input)

def log_output(log, input, target_output, output, stderr):
    if "good" not in log:
        log["good"] = 0
    if "bad" not in log:
        log["bad"] = []
    if stdout != target_output or stderr: 
        log["bad"].append([input, target_output, output, stderr])
    else:
        log["good"] += 1

def log2html(log):
    with open("log_%s.html"%log["id"],"w") as file:
        file.write("<b>ID:</b> %d <br>" % (log["id"]))

        if "compile_error" in log:
            file.write("<b>COMPILE ERROR:</b> %s <br>" % (log["compile_error"]))            
        else:   
            file.write("<b>MAIN CLASS:</b> %s <br>" % (log["classname"]))
            file.write("<b>GOOD RATIO:</b> %d/%d <br>" % (log["good"], log["good"] + len(log["bad"])))
            file.write("<b>TEST DURATIOn:</b> %f s<br>" % (log["endtime"] - log["starttime"]))
            
            file.write('<table border="1">')
            file.write("<tr>")
            file.write("<th>INPUT</th><th>TARGET_OUTPUT</th><th>OUTPUT</th><th>ERROR</th>")
            file.write("</tr>")
            for row in log["bad"]:
                file.write("<tr>")
                for item in row:
                    file.write("<td>")
                    file.write(item.replace("\n","<br>"))
                    file.write("</td>")
                file.write("</tr>")
            file.write("</table>")




for hw_id, hw_details in hw_data.iteritems():
    if isinstance(hw_details['testcases'], basestring):
        with open(hw_details['testcases'],"r") as data_file:        
            hw_details['testcases'] = json.load(data_file)

    for submission_id in get_new_submissions(hw_id):
        print("Testing submission: %d" % submission_id)
        log = {}
        log["id"] = submission_id

        data = get_submission_file(submission_id)
        
        src_dir = EXTRACT_DIR + str(submission_id)

        clean_dir(src_dir)
        clean_dir(WORKING_DIR)

        try:
            unzip(data, src_dir)
            (stdout, stderr) = java_compile_all(src_dir, WORKING_DIR)
            if stderr:
                log["compile_error"] = stderr   
        except Exception as e:
            log["compile_error"] = e                            

        if "compile_error" not in log:
            target = find_java_class_with_package(hw_details['classname'], WORKING_DIR)       
            log["classname"] = target

            testcntr = 0
            log["starttime"] = time.clock()
            for input,target_output in hw_details['testcases'].iteritems():            
                testcntr += 1
                if (testcntr > hw_details["max testcount"]):
                    break
                (stdout, stderr, extraerr) = run_firejail_java(target,input,hw_details['firejail profile'], timeout = hw_details['timeout'])
                stdout = stdout.strip()
                target_output = target_output.strip()

                log_output(log, input, target_output, stdout, stderr or extraerr)

                if break_on_first_error and (stdout != target_output or stderr or extraerr):                
                    break            
                                
                if break_on_first_timeout and extraerr:
                    break    
                
            log["endtime"] = time.clock()

            if enable_write_to_database:
                if stderr or extraerr:
                    post_result(submission_id, CORRECTOR_NAME, 9, 0, truncate(stderr))
                elif stdout != target_output:
                    post_result(submission_id, CORRECTOR_NAME, 7, 0, bad_output_message(stdout, input))
                else:
                    post_result(submission_id, CORRECTOR_NAME, 7, hw_details['fullscore'], "Passed all tests.")
        else:
            if enable_write_to_database:
                post_result(submission_id, CORRECTOR_NAME, 9, 0, truncate(log["compile_error"]))            
        if log_to_html:
            log2html(log)    


       
