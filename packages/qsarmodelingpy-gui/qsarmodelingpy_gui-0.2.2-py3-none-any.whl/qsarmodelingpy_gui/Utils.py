import os
import sys
from pathlib import Path
import logging
import tempfile
import shutil
import subprocess
import time
import platform
import configparser
from typing import Optional, Union
__DIR__ = Path(getattr(sys, '_MEIPASS', Path(__file__).parent.resolve()))

TMP_DIRECTORY: Optional[str] = None
LOG_FILE: Optional[str]  = None


def __initialize_temporary_file() -> str:
    global LOG_FILE
    LOG_FILE = os.path.join(get_tmp(), "qsarmodeling.log")
    open(LOG_FILE, "w").close()
    return LOG_FILE


def get_log_file() -> str:
    if LOG_FILE is None:
        return __initialize_temporary_file()
    else:
        return LOG_FILE


def get_tmp() -> str:
    global TMP_DIRECTORY
    if TMP_DIRECTORY is None:
        TMP_DIRECTORY = tempfile.mkdtemp()
    return TMP_DIRECTORY


def cleanup_temporary_directory() -> None:
    global TMP_DIRECTORY
    if TMP_DIRECTORY is not None:
        shutil.rmtree(TMP_DIRECTORY)
        TMP_DIRECTORY = None


def open_external(filepath: str) -> None:
    """Open an external file with the default software.
    Args:
        filepath (str): The file path to open
    """
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath) # type: ignore
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))


def get_config_filename(filename=None) -> Union[Path, None]:
    """Look for the configuration file and return the path if found.

    Args:
        filename (str | Path | None, optional): the filename to use as default (if this is given and the file exists, it'll be returned). Defaults to None.

    Returns:
        Path: The Path to the configuration file, or None if not found.
    """
    if filename is not None and Path(filename).is_file():
        return Path(filename)

    LOOKUP = [Path("./qsarmodelingpy.conf"),
              Path("~/qsarmodelingpy.conf").expanduser(),
              Path("~/.qsarmodelingpy.conf").expanduser(),
              Path("./qsarmodeling.conf"),
              Path("~/qsarmodeling.conf").expanduser(),
              Path("~/.qsarmodeling.conf").expanduser(),
              __DIR__ / "qsarmodelingpy.conf"
              ]
    for path in LOOKUP:
        if path.resolve().is_file():
            logging.info(f"Loaded {path.resolve()} as the configuration file.")
            return path
    return None


def read_config(section: str = None, key: str = None, filename: Union[Path, str, None] = None) -> Union[str, dict]:
    """Reads a configuration file.

    Args:
        section (str): The section of the configuration file. If None, the whole file is returned.
        key (str): The key of the configuration file. If None, the whole section is returned.

    Returns:
        str: The value of the configuration file. If the file or section/key doesn't exist, an empty dict is returned.
    """
    filename = get_config_filename(filename)
    if filename is None:
        return {}
    parser = configparser.ConfigParser()
    parser.read(filename)
    if section is None:
        if key is not None:
            for sec in parser.sections():
                if key in parser[sec]:
                    return parser[sec][key]
            return {}
        return {section: dict(parser[section]) for section in parser.sections()}
    elif section not in parser.sections():
        return {}
    elif key is None:
        return dict(parser[section])
    else:
        return parser[section][key] if key in parser[section] else {}


# GUI Handlers
def set_output_matrix_as_input(self, config) -> None:
    """Sets the output matrix as input in the GUI.

    It's particularly useful at the end of a calculation, when you want that the result is shown in the GUI.
    """
    if os.path.isfile(config['output_matrix']):
        self.handler.set_X_matrix(config['output_matrix'])
        self.draw_matrices('matrix')
    if self.running_process is not None:
        self.running_process.terminate()
    self.running_process = None


def get_current_time_as_string() -> str:
    """Returns the current time as a string.

    Returns:
        str: The current time as a string.
    """
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())