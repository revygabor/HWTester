import os
from StringIO import StringIO
from zipfile import ZipFile
import subprocess
import shutil
import fcntl
import time
import signal
import imp

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

def run(command_with_arguments, input, timeout = 5.0):
    sp = subprocess.Popen(command_with_arguments.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=4096, preexec_fn=os.setsid)
    starttime = time.clock()

    file_flags = fcntl.fcntl(sp.stdout.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stdout.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    file_flags = fcntl.fcntl(sp.stderr.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stderr.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    extraerrList = []
    stdoutList = []
    stderrList = []
    try:
        sp.stdin.write(input)
        sp.stdin.close()

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
    except:
        extraerrList.append("Cannot write input to program, broken pipe!\n")

    #sp.communicate(input=input)
    return ("".join(stdoutList), "".join(stderrList), "".join(extraerrList))

def run_firejail(command_with_arguments, input, firejail_profile_file=None, timeout = 5.0):
    params = ["firejail", "--quiet"]
    if firejail_profile_file:
        params.append("--profile=%s" % firejail_profile_file)
    params.extend(command_with_arguments.split())
    return run(" ".join(params), input=input, timeout=timeout)


def get_class(classpath):
    if not classpath.endswith(".py"):
        classpath = classpath + ".py"
    modname = os.path.basename(classpath).replace(".py", "")
    mod = evaluatormod = imp.load_source(modname, classpath)
    clazz = getattr(mod, modname)
    return clazz
