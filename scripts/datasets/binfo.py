class Binfo():
    """
        Binfo – short for Bin Info
        Stores information on a given dataset for multiple bin files
    """

    def __init__(self, label):
        self.label = label
        self.bins = {}

    def set_file_location(self, path):
        self.path = path

    def add_bin(self, filename, height, width, depth, timesteps):
        self.bins[filename] = (height, width, depth, timesteps)
