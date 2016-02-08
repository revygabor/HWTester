from connection_hfportal import get_new_submissions, get_submission_file, post_result

subms = get_new_submissions(47)
print(subms)


data = get_submission_file(subms[0])
print("length of file: %d" % len(data))

result = post_result(subms[0], "HWTester", 7, 25, "lorem ipsum")
print(result)
