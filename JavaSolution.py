import Solution
import subprocess
import os
import Utility

class JavaSolution(Solution.Solution):
    def __init__(self, src_dir, bin_dir, firejail_profile_file=None):
        self.__src_dir = src_dir
        self.__bin_dir = bin_dir
        self.__firejail_profile_file = firejail_profile_file
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
            "find %s -name \*.java -not -path '*/\.*' -print0 | xargs -0 javac -encoding ISO8859_1 -d %s" % (self.__src_dir.replace(" ","\\ "), self.__bin_dir.replace(" ","\\ ")), shell=True,
            executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return sp.communicate()

    def __find_java_class_with_package(self, name):
        fullname = name + ".class"
        for root, dirs, files in os.walk(self.__bin_dir):
            if fullname in files:
                tmp = root.split(os.sep)[1:]
                tmp.append(name)
                return ".".join(tmp)
        return None

    def __run_firejail_java(self, classname, input, timeout=5.0):
        classpath = "."
        return Utility.run_firejail("java -Djava.security.manager -cp %s %s" % (classpath, classname), input,
                                    self.__firejail_profile_file, timeout=timeout)

    def prepare(self):
        return self.__java_compile_all()

    def find_runnable(self, project_name):
        return self.__find_java_class_with_package(project_name)

    def run(self, classname, input, timeout=5.0):
        return self.__run_firejail_java(classname, input, timeout)