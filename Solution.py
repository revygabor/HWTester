class Solution(object):
    def prepare(self):
        raise NotImplementedError("not implemented")

    def find_runnable(self, project_name):
        raise NotImplementedError("not implemented")

    def run(self, runnable, input, timeout=5.0):
        raise NotImplementedError("not implemented")