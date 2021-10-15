import os

class HspiceResultFile:
    def __init__(self, basename):
        self.tran = basename + ".tr0"
        self.dc = basename + ".sw0"
        self.measure = basename + ".mt0"

def run(file_path):
    basename, ext = os.path.splitext(file_path)

    command = "hspice.exe -i {0}".format(file_path)
    print(command)
    os.system(command)

    return HspiceResultFile(basename)
