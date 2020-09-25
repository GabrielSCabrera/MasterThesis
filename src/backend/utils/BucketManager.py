from pathlib import Path
from typing import List
from os import environ
import requests

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage

from ..utils.terminal import reset_screen, B, I
from ..utils.select import scroll_select, select_bool
from ..utils.parsers import format_bytes
from ..config import config, defaults

class BucketManager:
    '''
        Constructorless class for managing local vs. remote files.
    '''

    credentials_active = False

    @classmethod
    def sync(cls, verbose:bool = True, force:bool = False) -> None:
        '''
            Synchronizes the local filesystem with the remote filesystem
            without overwriting already downloaded data.
        '''
        local_files = cls._inspect_files_local()
        remote_files = cls._inspect_files_remote()

        if local_files != remote_files or force:
            for i in remote_files:
                condition = i not in local_files.keys() or local_files[i] != remote_files[i]
                if verbose:
                    if i not in local_files.keys() or force:
                        size = f'[{format_bytes(remote_files[i])}]'
                        msg = B(f'Downloading File {size:>8s}: ') + I(str(i))
                        print(msg)
                    elif local_files[i] != remote_files[i]:
                        size = f'[{format_bytes(remote_files[i])}]'
                        msg = B(f'   Updating File {size:>8s}: ') + I(str(i))
                        print(msg)
                if condition or force:
                    remote_path = 'https://' + str(config.data_url / i)
                    local_path = config.data_path / i
                    with open(local_path, 'wb+') as outfile:
                        outfile.write(cls._download_file(remote_path))
        elif verbose:
            print(B('Already Up-To-Date'))

    @classmethod
    def login(cls, directory:Path = None) -> None:
        '''
            Interactive user login through CLI.
        '''
        reset_screen()
        if directory is None:
            directory = config.credentials_path
        files = []
        for f in cls._get_keys(directory):
            files.append(f.name)

        N = len(files)
        if N == 0:
            msg = (
                f'No Credential Files Available – save GCP .json file to '
                f'directory `{str(config.credentials_path)}` and try again.'
            )
            raise FileNotFoundError(msg)
        elif N == 1:
            selection = select_bool(f'Use Credentials File `{files[0]}`?')
            if not selection:
                print('Terminating.')
                exit()
            else:
                selection = files[0]
        else:
            selection = scroll_select(
                f'Select a Credentials File – {N} option(s)', files
            )
            path = directory / selection

        reset_screen()
        print(B('Selected file: ') + I(selection))
        print(
            B('Validating Credentials'), end = '',
            flush = True
        )

        cls.autologin(selection, directory)
        print(B(' – Success!'))

    @classmethod
    def autologin(cls, filename:str, directory:Path = None) -> None:
        '''
            Explicit login using GCP credentials .json filename.
        '''
        if directory is None:
            directory = config.credentials_path

        path = directory / filename

        if not path.exists():
            msg = (
                f'\n\n{B("Attempted to log in with non-existent file: ")}'
                f'\n{I(path)}'
            )
            raise FileNotFoundError(msg)

        environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(path)

        success = False
        try:
            client = storage.Client()
            success = True
        except DefaultCredentialsError:
            pass

        if not success:
            msg = (
                f'\n\n{B("Unable to validate credentials for file: ")}'
                f'{I(selection)}\n{B("Check integrity of file ")}'
                f'{B("and confirm credentials are still valid on GCP.")}'
            )
            raise DefaultCredentialsError(msg)
        else:
            cls.credentials_active = True

    @classmethod
    def _inspect_files_local(cls, directories:List = None):
        '''
            Returns a dict containing filesize information:

                    sizes = {
                        directory_1: {
                            filename_1 : size,
                            filename_2 : size, ...
                        },
                        directory_2: {
                            filename_3 : size,
                            filename_4 : size, ...
                        }, ...
                    }
        '''
        if directories is None:
            directories = [
                config.density_data_relpath, config.bins_relpath,
                config.input_txts_relpath
            ]
        sizes = {}
        for i in directories:
            files = i.glob("*")
            for f in files:
                key = '/'.join(str(f).split('/')[-2:])
                sizes[key] = f.stat().st_size
        return sizes

    @classmethod
    def _inspect_files_remote(cls, data_bucket_files:List = None):
        '''
            Returns a dict containing filesize information:

                    sizes = {
                        directory_1: {
                            filename_1 : size,
                            filename_2 : size, ...
                        },
                        directory_2: {
                            filename_3 : size,
                            filename_4 : size, ...
                        }, ...
                    }
        '''
        if data_bucket_files is None:
            data_bucket_files = defaults.data_bucket_files
        sizes = {}
        for i in data_bucket_files:
            path = 'https://' + str(config.data_url / i)
            sizes[str(i)] = int(requests.get(path, stream = True).headers['Content-length'])
        return sizes

    @classmethod
    def download(cls, dataset:str, force:bool = False, verbose:bool = True):
        '''
            Allows users to download data from a particular dataset to their
            local filesystem.  Only performs download if filesizes do not match,
            unless 'force' is True.
        '''
        datasets_remote = {
            'density_data' : [
                Path('density_data') / 'damage_WG02_s25.txt',
                Path('density_data') / 'damage_WG04_s25.txt',
                Path('density_data') / 'damage_MONZ4_s25.txt',
                Path('density_data') / 'damage_M8_2_s25.txt',
                Path('density_data') / 'damage_M8_1_s25.txt',
                Path('density_data') / 'damage_MONZ5_s25.txt',
                Path('density_data') / 'damage_MONZ3_s25.txt',
                Path('density_data') / 'damage_WG01_s25.txt',
            ],
            'bins' : [
                Path('bins') / 'WG04_bins.zip',
                Path('bins') / 'MONZ5_bins.zip',
                Path('bins') / 'M8_2_bins.zip',
                Path('bins') / 'M8_1_bins.zip'
            ],
            'input_txts' : [
                Path('input_txts') / 'WG04_3D_frac_full_a3000.txt',
                Path('input_txts') / 'MONZ5_3D_frac_full_a500.txt',
                Path('input_txts') / 'WG04_3D_frac_full_a500.txt',
                Path('input_txts') / 'MONZ5_3D_frac_full_a1000.txt',
                Path('input_txts') / 'M8_2_3D_frac_full_a500.txt',
                Path('input_txts') / 'M8_1_3D_frac_full_a1000.txt',
                Path('input_txts') / 'MONZ5_3D_frac_full_a2000.txt',
                Path('input_txts') / 'M8_2_3D_frac_full_a3000.txt',
                Path('input_txts') / 'M8_2_3D_frac_full_a1000.txt',
                Path('input_txts') / 'M8_1_3D_frac_full_a3000.txt',
                Path('input_txts') / 'MONZ5_3D_frac_full_a3000.txt',
                Path('input_txts') / 'WG04_3D_frac_full_a2000.txt',
                Path('input_txts') / 'M8_1_3D_frac_full_a2000.txt',
                Path('input_txts') / 'WG04_3D_frac_full_a1000.txt',
                Path('input_txts') / 'M8_1_3D_frac_full_a500.txt',
                Path('input_txts') / 'M8_2_3D_frac_full_a2000.txt',
            ]
        }

        datasets_local = {
            'density_data' : [config.density_data_relpath,],
            'bins' : [config.bins_relpath,],
        }

        local_files = cls._inspect_files_local(datasets_local[dataset])
        remote_files = cls._inspect_files_remote(datasets_remote[dataset])

        if verbose:
            print(B('Synchronizing Data Files'))

        if local_files != remote_files or force:
            for i in remote_files:
                condition = i not in local_files.keys() or local_files[i] != remote_files[i]
                if verbose:
                    if i not in local_files.keys() or force:
                        size = f'[{format_bytes(remote_files[i])}]'
                        msg = B(f'Downloading File {size:>8s}: ') + I(str(i))
                        print(msg)
                    elif local_files[i] != remote_files[i]:
                        size = f'[{format_bytes(remote_files[i])}]'
                        msg = B(f'   Updating File {size:>8s}: ') + I(str(i))
                        print(msg)
                if condition or force:
                    remote_path = 'https://' + str(config.data_url / i)
                    local_path = config.data_path / i
                    with open(local_path, 'wb+') as outfile:
                        outfile.write(cls._download_file(remote_path))
        elif verbose:
            print(B('Already Up-To-Date'))

    @classmethod
    def _download_file(cls, url:str):
        '''
            Downloads the file at the given url and returns the data.
        '''
        return requests.get(url, allow_redirects = False).content

    @classmethod
    def _get_keys(cls, directory:Path = None) -> List[Path]:
        '''
            Returns a list of Path instances linked to .json files containing
            user credentials, in the given directory.
        '''
        if not directory.is_dir():
            msg = (
                'Parameter `directory` expects a path to an existing directory.'
            )
            raise IOError(msg)

        files = directory.glob('*')
        return files

    @classmethod
    def logout(cls):
        '''
            Logs the user out.
        '''
        del environ["GOOGLE_APPLICATION_CREDENTIALS"]
        cls.credentials_active = False
