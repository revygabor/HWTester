import Solution
import os

class TextSolution(Solution.Solution):
    def __init__(self, src_dir, bin_dir, firejail_profile_file=None):
        self.__src_dir = src_dir
        pass

    def prepare(self):
        return ("","")

    def find_runnable(self, project_name):
        fullname = project_name + ".txt"
        for root, dirs, files in os.walk(self.__src_dir):
            if fullname in files:
                return (os.path.join(root, fullname), None)
        return (None, "Cannot find file %s !" % fullname)

    def run(self, path, input, timeout=5.0):
        data = ""
        with open(path, "r") as data_file:
            data = data_file.read()
        return (data,"","")