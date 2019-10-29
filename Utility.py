import os
from StringIO import StringIO
from zipfile import ZipFile
import subprocess
import shutil
import fcntl
import time
import signal
import imp
import sys,traceback
def dir_clean_error(function,path,excinfo):
    print 'WARNING: Ran into issues trying to remove directory:',path,str(function),str(excinfo)

def clean_dir(target_dir):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True,onerror= dir_clean_error)

def unzip(data, target_dir, filename=None):
    submission_zipfile = ZipFile(StringIO(data))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if filename:
        submission_zipfile.extract(filename,target_dir)
    else:
        submission_zipfile.extractall(target_dir)
        
def magic_quote_splitter(params):
    # hftester -param "hehehe" -v "path  to file here":/usr/src/myapp -
    out = []
    
    inquotes = False
    for i,param in enumerate(params.split()):

        if inquotes:
            out[-1]+=' ' +str(param)
        else:
            out+=[str(param)]
            
        for c in param:
            if c == '"' or c =='\'':
                inquotes = not inquotes            
        
    print 'magic_quote_splitter: ',out
    return out  
        
def run(command_with_arguments, input, timeout = 5.0, dockercleanup = False):
    if dockercleanup:
        cleanup_cmd = "docker rm -f hftester"
        print "Running docker cleanup:",cleanup_cmd
        os.system(cleanup_cmd)
    pipe_buffer_size = 4096
    if len(input) > pipe_buffer_size:
        stdin_buffer_file = open('stdin_buffer_file.tmp','w')
        stdin_buffer_file.write(input)
        stdin_buffer_file.close()
        stdin_buffer_file = open('stdin_buffer_file.tmp')
        sp = subprocess.Popen(magic_quote_splitter(command_with_arguments), stdin=stdin_buffer_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=pipe_buffer_size, preexec_fn=os.setsid, universal_newlines = True)
    else:
        sp = subprocess.Popen(magic_quote_splitter(command_with_arguments), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=pipe_buffer_size, preexec_fn=os.setsid)
    starttime = time.clock()

    file_flags = fcntl.fcntl(sp.stdout.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stdout.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    file_flags = fcntl.fcntl(sp.stderr.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sp.stderr.fileno(), fcntl.F_SETFL, file_flags | os.O_NDELAY)

    extraerrList = []
    stdoutList = []
    stderrList = []
    linecount = 0
    try:
        #for line in input.split('\n'):
        #    print linecount,line
        if (len(input) <= pipe_buffer_size):
            sp.stdin.write(input)
            sp.stdin.close()
        #time.sleep(1)
        #sp.stdin.flush()

        totalOutput = 0

        while totalOutput < 4096 * 1024 and sp.poll() is None and time.clock() - starttime < timeout:
            try:
                r = sp.stdout.read()
                totalOutput = totalOutput + len(r)
                stdoutList.append(r)
            except IOError:
                pass
            except Exception, e:
                print 'stdout:',sys.exc_info()
                pass
            try:
                r = sp.stderr.read()
                totalOutput = totalOutput + len(r)
                stderrList.append(r)
            except IOError:
                pass
            except Exception, e:
                print 'stderr:',sys.exc_info()
                pass

        if sp.poll() is None:
            if totalOutput >= 4096 * 1024:
                extraerrList.append("Too much output data received, killing process!\n")
            if time.clock() - starttime >= timeout:
                extraerrList.append("Maximum allowed time exceeded, killing process! First 10000 chars of input was: [%s]\n"%(input[0:min(10000,len(input))]))
            os.killpg(os.getpgid(sp.pid), signal.SIGTERM)
            #sp.kill()
    #except ValueError:
        #pass
        
    except Exception, e:
        print sys.exc_info()
        extraerrList.append("Error:"+str(e))
        joined_extraerrors = '\n'.join(extraerrList)
        print 'extraerrList:',joined_extraerrors[0:min(200,len(joined_extraerrors))]
        #raise e
    
    joined_extraerrors = '\n'.join(extraerrList)
    if len(stderrList)>0 or len(extraerrList)>0:
        print "Finished running command sdterr and extraerr:", "".join(stderrList), joined_extraerrors[0:min(200,len(joined_extraerrors))]
    #sp.communicate(input=input)
    return ("".join(stdoutList), "".join(stderrList), "".join(extraerrList))

def run_firejail(command_with_arguments, input, firejail_profile_file=None, timeout = 5.0):
    params = ["firejail", "--quiet"]
    if firejail_profile_file:
        params.append("--profile=%s" % firejail_profile_file)
    params.extend(command_with_arguments.split())
    return run(" ".join(params), input=input, timeout=timeout)

def run_python_docker(python_file_path, input, firejail_profile_file=None, timeout = 5.0):
    pydir, sep, pyfilename = python_file_path.rpartition(os.sep)
    cmd = 'timeout -s KILL %d docker run -i --rm --name hftester -v %s:/usr/src/myapp -w /usr/src/myapp python:3-alpine python %s'%(timeout,pydir, pyfilename)
    print 'Running python docker command',cmd
    #return None 
    
    return run(cmd, input=input,timeout = timeout,dockercleanup = True)
   
def get_class(classpath):
    if not classpath.endswith(".py"):
        classpath = classpath + ".py"
    modname = os.path.basename(classpath).replace(".py", "")
    mod = evaluatormod = imp.load_source(modname, classpath)
    clazz = getattr(mod, modname)
    return clazz
