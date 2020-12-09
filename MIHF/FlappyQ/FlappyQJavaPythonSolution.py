import os
import subprocess

import JavaPythonSolution
import Utility

project_root = os.path.abspath(os.path.join('MIHF', 'FlappyQ'))
eval_py_files = os.path.join(project_root, 'py_files')
eval_java_files = os.path.join(project_root, 'java_files', '*.java')
docker_folder = 'py_files'

class FlappyQJavaPythonSolution(JavaPythonSolution.JavaPythonSolution):
    def __init__(self, src_dir, bin_dir, firejail_profile_file=None):
        super(FlappyQJavaPythonSolution, self).__init__(src_dir, bin_dir, firejail_profile_file)
        self.__src_dir = src_dir
        self.__bin_dir = bin_dir  # WORKING_DIR
        self.__firejail_profile_file = firejail_profile_file
        self.javaOrPython = None
        pass

    def java_compile_all(self):
        if not os.path.exists(self.__bin_dir):
            os.makedirs(self.__bin_dir)
        print 'java compile test'
        sp = subprocess.Popen(
            "cp %s %s" % (eval_java_files, self.__src_dir.replace(" ", "\\ ")), shell=True,
            executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = sp.communicate()

        if not stderr:
            sp = subprocess.Popen(
                "find %s -name \*.java -not -path '*/\.*' -print0 | xargs -0 javac -nowarn -encoding ISO8859_1 -d %s" % (
                    self.__src_dir.replace(" ", "\\ "), self.__bin_dir.replace(" ", "\\ ")), shell=True,
                executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = sp.communicate()

        if stderr:
            new_stderr = []
            for line in stderr.split("\n"):
                if not line.startswith("Note:"):
                    new_stderr.append(line)
            stderr = "\n".join(new_stderr)
        return (stdout, stderr)

    def run(self, classname, input, timeout=5.0):
        if self.javaOrPython == 'java':
            return self.__run_firejail_java(classname, input, timeout)
        else:
            return self.run_python_docker(classname, timeout=timeout)

    def run_python_docker(self, python_file_path, timeout=5.0):
        cmd = 'docker run -i --rm -m 400M --memory-swap -1 --ulimit cpu=%d ' \
              '--name hftester -v %s:/%s:ro ' \
              '-v %s:/%s/flappy_agent.py ' \
              'python:3-alpine-numpy python %s/flappy_evaluator_server.py' \
              % (timeout, eval_py_files, docker_folder, python_file_path, docker_folder, docker_folder)

        print 'Running python docker command', cmd

        return Utility.run(cmd, input="", timeout=timeout, dockercleanup=True)






    def __find_java_class_with_package(self, name):
        fullname = name + ".class"
        for root, dirs, files in os.walk(self.__bin_dir):
            if fullname in files:
                reldir = os.path.relpath(root,self.__bin_dir)
                tmp = reldir.split(os.sep)
                if (reldir=="."):
                    tmp = []
                tmp.append(name)
                return (".".join(tmp), None)
        return (None, "Cannot find class %s with main() function." % name)
    def __find_python_file(self, name):
        fullname = name + ".py"
        for root, dirs, files in os.walk(self.__bin_dir):
            if fullname in files:
                reldir = os.path.relpath(root,self.__bin_dir)
                tmp = reldir.split(os.sep)
                if (reldir=="."):
                    tmp = []
                tmp.append(name)
                return (".".join(tmp), None)
        return (None, "Cannot find file %s" % fullname)

    def __run_firejail_java(self, classname, input, timeout=5.0):
        classpath = "."
        return Utility.run_firejail("java -Djava.security.manager -cp %s %s" % (classpath, classname), input,
                                    self.__firejail_profile_file, timeout=timeout)

    def run_java(self, classname, input, timeout=5.0):
        classpath = self.__bin_dir
        return Utility.run("java -Djava.security.manager -cp %s %s" % (classpath, classname), input, timeout=timeout)

    def prepare(self):
        #has already been unzipped at this point, time to check for python or .java
        self.javaOrPython = "java"
        
        for file in os.listdir(self.__src_dir):
            if file.endswith(".py"):
                self.javaOrPython = "python"
                self.__bin_dir = self.__src_dir + os.sep + file
                print "Python solution found at",self.__bin_dir
                break
        if self.javaOrPython == "python":
            return ("Python","")
        else:
            return self.java_compile_all()

    def find_runnable(self, project_name):
        if self.javaOrPython == 'java':
            return self.__find_java_class_with_package(project_name)
        elif self.javaOrPython == 'python':
            return (self.__bin_dir,None)
        else:
            return (None,"Could not determine solution type. No .py or java files found!")
