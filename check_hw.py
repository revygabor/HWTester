from connection_hfportal import get_new_submissions, get_submission_file, post_result
from prepare_hw import unzip, java_compile, run_firejail_java, java_compile_all, clean_dir

def get_tests_for_hw(hw_id):
    return {'aaaa': 'aaaa', 'bbbb': 'bbbb'}



HW_IDS = [47]

for hw_id in HW_IDS:
    for submission_id in get_new_submissions(hw_id):
        print(submission_id)
        data = get_submission_file(submission_id)
        
        #try
        unzip(data, "secure")

        (stdout, stderr) = java_compile_all("secure")
        if stderr:
            post_result(submission_id, "HWTester", 9, 0, stderr)
            break

        for input,target_output in get_tests_for_hw(hw_id).iteritems():            
            (stdout, stderr) = run_firejail_java("test",input,"secure_firejail_profile")
            if stdout.strip() != target_output.strip() or stderr:                
                break            

        if stderr:
            post_result(submission_id, "HWTester", 9, 0, stderr)
            break
        if stdout.strip() != target_output.strip():
            post_result(submission_id, "HWTester", 7, 0, stdout)
            break

        post_result(submission_id, "HWTester", 7, 25, "ok")

