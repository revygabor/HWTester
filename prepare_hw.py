import os
from StringIO import StringIO
from zipfile import ZipFile
import subprocess
import shutil

def clean_dir(target_dir):
    shutil.rmtree(target_dir)

def unzip(data, target_dir, filename=None):
    submission_zipfile = ZipFile(StringIO(data))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if filename:
        submission_zipfile.extract(filename,target_dir)        
    else:
        submission_zipfile.extractall(target_dir)
        
def java_compile(filenames):
    sp = subprocess.Popen(["javac"].extend(filenames), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sp.communicate()

def java_compile_all(directory):        
    sp = subprocess.Popen("find %s -name \*.java -print0 | xargs -0 javac" % directory, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sp.communicate()

def run_firejail(command_with_arguments, input, firejail_profile_file=None):
    params = ["firejail", "--quiet"]
    if firejail_profile_file:
        params.append("--profile=%s" % firejail_profile_file)
    params.extend(command_with_arguments.split())

    sp = subprocess.Popen(params, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
    return sp.communicate(input=input)

def run_firejail_java(classname, input, firejail_profile_file=None):    
    return run_firejail("java -Djava.security.manager -cp . %s" % classname, input, firejail_profile_file)


