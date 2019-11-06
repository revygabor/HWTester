import Solution
import subprocess
import os
import Utility

class JavaPythonSolution(Solution.Solution):
    def __init__(self, src_dir, bin_dir, firejail_profile_file=None):
        self.__src_dir = src_dir
        self.__bin_dir = bin_dir #WORKING_DIR
        self.__firejail_profile_file = firejail_profile_file
        self.javaOrPython = None
        pass

    """
    def __java_compile(self, filenames):
        sp = subprocess.Popen(["javac", "-encoding", "UTF8"].extend(filenames), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        return sp.communicate()
    """

    def __java_compile_all(self):
        if not os.path.exists(self.__bin_dir):
            os.makedirs(self.__bin_dir)
        sp = subprocess.Popen(
            "find %s -name \*.java -not -path '*/\.*' -print0 | xargs -0 javac -nowarn -encoding ISO8859_1 -d %s" % (self.__src_dir.replace(" ","\\ "), self.__bin_dir.replace(" ","\\ ")), shell=True,
            executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = sp.communicate()
        if stderr:
            new_stderr = []
            for line in stderr.split("\n"):
                if not line.startswith("Note:"):
                    new_stderr.append(line)
            stderr="\n".join(new_stderr)
        return (stdout, stderr)

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
            return self.__java_compile_all()

    def find_runnable(self, project_name):
        if self.javaOrPython == 'java':
            return self.__find_java_class_with_package(project_name)
        elif self.javaOrPython == 'python':
            return (self.__bin_dir,None)
        else:
            return (None,"Could not determine solution type. No .py or java files found!")

    def run(self, classname, input, timeout=5.0):
        if self.javaOrPython == 'java':
            return self.__run_firejail_java(classname, input, timeout)        
        else:
            return Utility.run_python_docker(classname,input, firejail_profile_file=None, timeout = timeout)
    