
from ..utils.terminal import B, I, reset_screen
from ..utils.parsers import format_bytes
from ..utils.select import select_bool
from shutil import rmtree
from . import config

def uninstall(verbose:bool = True):
    '''
        Is called from makefile when user wishes to remove all traces of the
        program from the filesystem, with exception to the directory containing
        the package files themselves.
    '''
    msg = (
        "Uninstaller removes downloaded data files, experiments, and all "
        "processed files."
    )
    msg = B(msg)

    data_files = list(config.bins_relpath.glob('*'))
    data_files += list(config.density_data_relpath.glob('*'))
    data_files += list(config.input_txts_relpath.glob('*'))
    data_files = list(set(data_files))
    size = format_bytes(sum(i.stat().st_size for i in data_files))
    count = len([f'{i.name}' for i in data_files])

    msg += I(
        f"\n\tData Contents: {count} data files for a total of {size}."
    )

    files = list(config.storage_path.rglob('**/*'))
    filtered_files = []
    for i in files:
        if i not in data_files and not i.is_dir():
            filtered_files.append(i)

    size = format_bytes(sum(i.stat().st_size for i in filtered_files))
    count = len([f'{i.name}' for i in filtered_files])

    msg += I(
        f"\n\tResults Contents: {count} files for a total of {size}.\n"
    )

    reset_screen()
    print(msg)
    selection = select_bool("Proceed with removal?")

    if selection:

        # Deleting Hidden Files
        if config.storage_path.exists():
            rmtree(config.storage_path)

        # Deleting User Files
        if config.hidden_path.exists():
            rmtree(config.hidden_path)
