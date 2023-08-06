import sys
import logging
import coloredlogs
from Constants import DEBUG_MODE
from Utils import get_log_file


def init():
    logging_level = logging.DEBUG if DEBUG_MODE else logging.INFO
    if not DEBUG_MODE:
        # redirect stderr and stdout to a temporary file
        LOG_FILE = get_log_file()
        print(f"Initialized log in {LOG_FILE}")
        sys.stdout = open(LOG_FILE, 'a')
        sys.stderr = sys.stdout

    coloredlogs.install(fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)
    coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}


def silence_matplotlib_logger():
    logging.getLogger('matplotlib').setLevel(logging.WARNING)