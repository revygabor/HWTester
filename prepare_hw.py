import os
from StringIO import StringIO
from zipfile import ZipFile
import subprocess
import shutil
import fcntl
import time
import signal

def clean_dir(target_dir):
    if os.path.exists(target_dir):
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
    sp = subprocess.Popen(["javac","-encoding","UTF8"].extend(filenames), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sp.communicate()

def java_compile_all(src_dir, bin_dir):    
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    sp = subprocess.Popen("find %s -name \*.java -print0 | xargs -0 javac -encoding ISO8859_1 -d %s"% (src_dir, bin_dir), shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sp.communicate()

def find_java_class_with_package(name, path):        
    fullname = name + ".class"
    for root, dirs, files in os.walk(path):        
        if fullname in files:
            tmp = root.split(os.sep)[1:]
            tmp.append(name)
            return ".".join(tmp)
    return None

def run_firejail(command_with_arguments, input, firejail_profile_file=None, timeout = 5.0):
    params = ["firejail", "--quiet"]
    if firejail_profile_file:
        params.append("--profile=%s" % firejail_profile_file)
    params.extend(command_with_arguments.split())

    sp = subprocess.Popen(params, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=4096, preexec_fn=os.setsid)        
    starttime = time.clock()

    file_flags = fcntl.fcntl(sp.stdout.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stdout.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    file_flags = fcntl.fcntl(sp.stderr.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stderr.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    sp.stdin.write(input)
    sp.stdin.close()

    stdoutList = []
    stderrList = []
    extraerrList = []
    totalOutput = 0

    while totalOutput < 4096 * 1024 and sp.poll() is None and time.clock() - starttime < timeout:
        try:
            r = sp.stdout.read()
            totalOutput = totalOutput + len(r)
            stdoutList.append(r)                        
        except:            
            pass
        try:
            r = sp.stderr.read()
            totalOutput = totalOutput + len(r)
            stderrList.append(r)            
        except:       
            pass

    if sp.poll() is None:
        if totalOutput >= 4096 * 1024:
            extraerrList.append("Too much output data received, killing process!\n")
        if time.clock() - starttime >= timeout:
            extraerrList.append("Maximum allowed time exceeded, killing process!\n")
        os.killpg(os.getpgid(sp.pid), signal.SIGTERM)
        #sp.kill()

    #sp.communicate(input=input)
    return ("".join(stdoutList), "".join(stderrList), "".join(extraerrList))

def run_firejail_java(classname, input, firejail_profile_file=None, classpath = ".", timeout = 5.0):
    return run_firejail("java -Djava.security.manager -cp %s %s" % (classpath, classname), input, firejail_profile_file, timeout = timeout)


