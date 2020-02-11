from zipfile import ZipFile
import numpy as np
import os

class Binfo():
    """
        Binfo – short for Bin Info – Stores information on a given dataset for
        multiple compressed binary files
    """

    def __init__(self, label, path, dims):
        # Name of dataset
        self.label = label
        # Path to compressed directory
        self.path = path
        # Image dimensions
        self.dims = dims
        # Accessing the compressed directory
        self.bin_dir = ZipFile(f'{self.path}.zip', 'r')
        # Extracting valid filenames for the compressed binaries and
        # identifying the pressures (MPa) in each filename and extracting them
        files_dict = {}
        for f in self.bin_dir.namelist():
            if ".bin" in f and "__MACOSX" not in f:
                label_len = len(f"bins/{self.label}") + 1
                MPa = f[label_len:-7]
                files_dict[MPa] = f
        # Determining the chronological order of the files and saving the
        # respective pressures
        self.pressures = sorted(files_dict.keys())
        # Reordering the files and saving them as attributes
        self.bins = [files_dict[p] for p in self.pressures]
        # Iterable length
        self.index = self.__len__()
        # Creating dummy array for quick slicing reference
        self.dummy_arr = np.arange(0, self.__len__(), 1)

    def __iter__(self):
        return self

    def __next__(self):
        self.index -= 1
        if self.index == 0:
            self.index = len(self.bins)
            raise StopIteration
        else:
            return self.__getitem__(self.index)

    def __len__(self):
        return len(self.bins)

    def __getitem__(self, index):

        if isinstance(index, int):
            length = self.__len__()
            if index >= length or index < -length:
                msg = (f'\n\nAttempt to access element {index} in array of '
                       f'length {self.__len__()}.')
                raise IndexError(msg)
            else:
                return self._process_bin(index)
        elif isinstance(index, (slice, np.ndarray)):
                indices = self.dummy_arr[index]
                data_array = []
                for idx in indices:
                    data_array.append(self._process_bin(idx))
                return data_array
        else:
            msg = (f'\n\nInvalid key passed to Binfo.__getitem__\n\tExpects '
                   f'argument of <class \'int\'>, <class \'slice\'>, or'
                   f'<class \'np.ndarray\'>\n\tGot argument \'{index}\' of '
                   f'{type(index)}')
            raise TypeError(msg)

    def _process_bin(self, index):
        data = self.bin_dir.open(self.bins[index], 'r')
        data = np.frombuffer(data.read(), dtype = np.uint8)
        data = data.reshape(self.dims[2], self.dims[0], self.dims[1])
        data = np.swapaxes(data, 0, 1)
        data = np.swapaxes(data, 1, 2)
        return data

    def get_ones(self, index):

        if isinstance(index, int):
            length = self.__len__()
            if index >= length or index < -length:
                msg = (f'\n\nAttempt to access element {index} in array of '
                       f'length {self.__len__()}.')
                raise IndexError(msg)
            else:
                data = self._process_bin(index)
                data = np.where(data == 1)
                return data

        elif isinstance(index, (slice, np.ndarray)):
                indices = self.dummy_arr[index]
                data_array = []
                for idx in indices:
                    data = self._process_bin(idx)
                    data = np.where(data == 1)
                    data_array.append(data)
                return data_array
        else:
            msg = (f'\n\nInvalid key passed to Binfo.__getitem__\n\tExpects '
                   f'argument of <class \'int\'>, <class \'slice\'>, or'
                   f'<class \'np.ndarray\'>\n\tGot argument \'{index}\' of '
                   f'{type(index)}')
            raise TypeError(msg)

    def iter_ones(self, index = slice(0)):

        if isinstance(index, int):
            length = self.__len__()
            if index >= length or index < -length:
                msg = (f'\n\nAttempt to access element {index} in array of '
                       f'length {self.__len__()}.')
                raise IndexError(msg)
            else:
                index = np.array([index])

        elif not isinstance(index, (slice, np.ndarray)):
            msg = (f'\n\nInvalid key passed to Binfo.__getitem__\n\tExpects '
                   f'argument of <class \'int\'>, <class \'slice\'>, or'
                   f'<class \'np.ndarray\'>\n\tGot argument \'{index}\' of '
                   f'{type(index)}')
            raise TypeError(msg)

        indices = self.dummy_arr[index]
        for idx in indices:
            data = self._process_bin(idx)
            data = np.where(data == 1)
            yield data

if __name__ == "__main__":
    pass
