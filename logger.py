""" Log all stdout to LOGGER+TIMESTAMP.txt (or the machine name in the cloud). Starts automatically upon import. """

import sys

from   socket     import gethostname
from   datetime   import datetime
from   os         import uname
from   subprocess import check_output

LOGFILE_NAME = ""   # Global log file name will be set upon import of module and instantiation of the _Logger class.

class _Logger(object):
    """ Private helper class. Do not try to use this directly."""

    @ staticmethod
    def make_fname(stamp_time=False):

        fname = 'LOGGER'

        if bool(str(uname()[0]) == 'Linux'):
            fname += '-' + gethostname()

        if stamp_time:
            ts = str(str(datetime.now())[:-10]).replace(' ', '-').replace(':', '-')
            ts = ts[:10] + '_' + ts[11:]
            fname += '-' + ts

        fname += '.txt'

        return fname

    def __init__(self):

        # Redirect STDOUT
        self.terminal = sys.stdout

        # Set log filename
        global LOGFILE_NAME
        LOGFILE_NAME = self.make_fname()   # might add unique timestamp

        # Write APPEND to Log
        self.logfile = open(LOGFILE_NAME, mode="a")

    def write(self, msg):

        # Write to terminal
        self.terminal.write(msg)           # allow coloring in the terminal

        # Define colors
        NORMAL = '\033[0m'
        BOLD = '\033[1m'
        FADE = '\033[2m'
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'

        COLOR_BLACK = '\033[90m'
        COLOR_RED = '\033[91m'
        COLOR_GREEN = '\033[92m'
        COLOR_YELLOW = '\033[93m'
        COLOR_BLUE = '\033[94m'
        COLOR_MAGENTA = '\033[95m'
        COLOR_CYAN = '\033[96m'
        COLOR_WHITE = '\033[97m'

        HI_WHITE = '\033[1m\033[9%sm\033[4%sm' % (0, 7)
        HI_BLACK = '\033[1m\033[9%sm\033[4%sm' % (7, 0)
        HI_RED = '\033[1m\033[9%sm\033[4%sm' % (7, 1)
        HI_GREEN = '\033[1m\033[9%sm\033[4%sm' % (7, 2)
        HI_YELLOW = '\033[1m\033[9%sm\033[4%sm' % (7, 3)
        HI_BLUE = '\033[1m\033[9%sm\033[4%sm' % (7, 4)
        HI_MAGENTA = '\033[1m\033[9%sm\033[4%sm' % (7, 5)
        HI_CYAN = '\033[1m\033[9%sm\033[4%sm' % (7, 6)

        # Strip off Colors  (no coloring in the logfile)
        for FRMT in [NORMAL, BOLD, FADE, ITALIC, UNDERLINE, COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW,
                     COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE, HI_WHITE, HI_BLACK, HI_RED, HI_GREEN,
                     HI_YELLOW, HI_BLUE, HI_MAGENTA, HI_CYAN, '[40m', '[41m', '[42m', '[43m', '[44m', '[45m', '[46m', '[47m']:
            try:
                plaintxt = str(msg).replace(FRMT, '')
            except:
                plaintxt = msg

        # Write to Log File
        self.logfile.write(plaintxt)
        self.logfile.flush()

    def flush(self):
        pass


# AUTO-START LOGGER ON IMPORT ------------------------------------------------------------------------------------------

try: width =  int(check_output(['stty', 'size']).split()[1])
except: width =  80
sys.stdout = _Logger()
command_line_args = ' '.join(sys.argv).split('/')[-1]
caption = str(gethostname()).upper() + ': ' + command_line_args
caption +=  str(str(datetime.now())[:-10]).rjust(width-len(caption))
print('=' * width)
print(caption)
print('=' * width)