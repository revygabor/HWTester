from connection_hfportal import get_new_submissions, get_submission_file, post_result
from prepare_hw import unzip, java_compile, run_firejail_java, java_compile_all, clean_dir

subms = get_new_submissions(47)
data = get_submission_file(subms[0])

#clean_dir("secure")

#unzip(data, "secure")

#print(java_compile("secure/*.java"))
print(java_compile_all("secure"))

print(run_firejail_java("test","lorem ipsum","secure_firejail_profile"))