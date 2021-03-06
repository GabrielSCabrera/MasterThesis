from zipfile import ZipFile
import numpy as np
import os
import re

import src.backend.config.config as config
import src.backend.config.defaults as defaults

class Binfo():
    """
        Binfo – short for Bin Info – Stores information on a given dataset for
        multiple compressed binary files
    """
    @classmethod
    def load_data(cls):
        '''
            Performs all the required data loading for the data specific to this
            thesis.
        '''
        bin_dirs = {
            "M8_1": config.bins_relpath / "M8_1_bins",
            "M8_2": config.bins_relpath / "M8_2_bins",
            "MONZ5": config.bins_relpath / "MONZ5_bins",
            "WG04": config.bins_relpath / "WG04_bins",
        }

        bin_dims = {
            "M8_1": (1000, 1000, 1200),
            "M8_2": (900, 900, 1200),
            "MONZ5": (800, 800, 1200),
            "WG04": (800, 800, 1200),
        }

        bin_stresses = {}
        bin_stresses["M8_1"] = np.concatenate(
            [np.arange(26, 82, 4), np.arange(80, 120, 2), np.arange(122, 132, 2)]
        )

        bin_stresses["M8_2"] = np.concatenate(
            [np.arange(152, 186), np.arange(187, 197)]
        )

        bin_stresses["MONZ5"] = np.concatenate(
            [
                [2, 5],
                np.arange(30, 45, 5),
                np.arange(40, 90, 5),
                np.arange(92, 132, 2),
                np.arange(131, 150),
                np.arange(150.5, 162, 0.5),
            ]
        )

        bin_stresses["WG04"] = np.concatenate(
            [
                [15],
                np.arange(15, 100, 5),
                np.arange(95, 115, 5),
                np.arange(112, 142, 2),
                [141],
                np.arange(144, 149),
                [
                    148.5,
                    149,
                    142,
                    143,
                    149.5,
                    149.5,
                    150,
                    150.5,
                    151,
                    151.5,
                    152,
                    152.5,
                ],
            ]
        )

        config.bins = {}
        for l in config.labels:
            config.bins[l] = cls(l, bin_dirs[l], bin_dims[l], bin_stresses[l])

        defaults.split_defaults = {
            'dataset'     :   config.bins['M8_1'],
            'splits'      :   None,
            'mode'        :   'slice',
            'test_size'   :   0.25,
            'limit'       :   1,
            'shuffle'     :   True
        }

    def __init__(self, label, path, dims, stresses):
        # Name of dataset
        self.label = label
        # Axial Stresses
        self.stresses = stresses
        # Time to Macroscopic Failures
        self.fail_times = self.get_fail_times()
        # Path to compressed directory
        self.path = path
        # Image dimensions
        self.dims = dims
        # Accessing the compressed directory
        self.bin_dir = ZipFile(f'{self.path}.zip', 'r')
        # Extracting valid filenames for the compressed binaries and
        # identifying the pressures (MPa) in each filename and extracting them
        files_dict = {}
        order = []
        self.pressures = []
        self.bins = []
        for f in self.bin_dir.namelist():
            if ".bin" in f and "__MACOSX" not in f:
                label_len = len(f"bins/{self.label}") + 1
                MPa = re.sub(f'bins/{self.label}_' + r'(.*)MPa\.bin', r'\1', f)
                files_dict[MPa] = f
                # In case the pressures aren't in order
                if '_' in MPa:
                    split_string = MPa.split('_')
                    order.append(split_string[0])
                    self.pressures.append(split_string[1])
                    self.bins.append(f)
        # Determining the chronological order of the files and saving the
        # respective pressures
        if len(self.pressures) > 0 and len(self.bins) > 0:
            order = np.array(order, dtype = np.float64)
            order = np.argsort(order)
            self.pressures = list(map(float, self.pressures))
            self.pressures = list(map(str, np.array(self.pressures)[order]))
            # Reordering the files and saving them as attributes
            self.bins = list(map(str, np.array(self.bins)[order]))
        else:
            order = list(map(float, files_dict.keys()))
            order = np.array(order, dtype = np.float64)
            order = np.argsort(order)
            self.pressures = list(map(str, np.array(list(files_dict.keys()))[order]))
            # Reordering the files and saving them as attributes
            self.bins = [files_dict[p] for p in self.pressures]
        # Iterable length
        self.index = self.__len__()
        # Creating dummy array for quick slicing reference
        self.dummy_arr = np.arange(0, self.__len__(), 1)
        # Number of time-steps in the dataset
        self.samples = len(self.pressures)

    def __iter__(self):
        return self

    def __next__(self):
        self.index -= 1
        if self.index == -1:
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

    def __str__(self):
        '''
            Returns the label of the current instance
        '''
        return self.label

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
                return np.array(data).T

        elif isinstance(index, (slice, np.ndarray)):
                indices = self.dummy_arr[index]
                data_array = []
                for idx in indices:
                    data = self._process_bin(idx)
                    data = np.where(data == 1)
                    data_array.append(np.array(data).T)
                return data_array
        else:
            msg = (f'\n\nInvalid key passed to Binfo.__getitem__\n\tExpects '
                   f'argument of <class \'int\'>, <class \'slice\'>, or'
                   f'<class \'np.ndarray\'>\n\tGot argument \'{index}\' of '
                   f'{type(index)}')
            raise TypeError(msg)

    def iter_ones(self, index = None):
        if index is None:
            index = slice(0, self.__len__(), 1)
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
            yield np.array(data).T

    def get_fail_times(self):
        """
            From 'extract_feat_frac_3D.m'
        """
        Pc = 10
        Poring = 13.43
        diff_stress = self.stresses*(25/16) - Pc - Poring
        fail_stress = 152.544*25/16 - 10 - Poring
        return (fail_stress-diff_stress)/fail_stress
