import os

class Binfo():
    """
        Binfo – short for Bin Info
        Stores information on a given dataset for multiple bin files
    """

    def __init__(self, label, path, dims):
        self.label = label
        self.path = path
        self.dims = dims

    def get_frames(self):
        # Finding all files in the given directory
        files = os.listdir(self.path)
        # Identifying the pressures (MPa) in each filename and extracting them
        files_dict = {}
        for f in files:
            label_len = len(self.label) + 1
            MPa = f[label_len:-7]
            files_dict[int(MPa)] = f
        # Determining the chronological order of the files and saving the
        # respective pressures
        self.pressures = sorted(files_dict.keys())
        # Reordering the files and saving them as attributes
        self.bins = [files_dict[p] for p in self.pressures]
