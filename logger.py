""" Log stdout to a file named 'LOG'+timestamp (or machine name if run in the cloud). Starts automatically upon import
"""

import sys

from   socket     import gethostname
from   datetime   import datetime
from   os         import uname

import ui

LOGFILE_NAME = ""

def logger_output_fname(add_timestamp=False):

    fname = 'LOGGER'

    if bool(str(uname()[0]) == 'Linux'):
        fname += '-' + gethostname()

    if add_timestamp:
        ts = str(str(datetime.now())[:-10]).replace(' ', '-').replace(':', '-')
        ts = ts[:10] + '_' + ts[11:]
        fname += '-' + ts

    fname += '.txt'

    return fname

class _Logger(object):
    """ Private helper class. Do not try to use this directly."""

    def __init__(self):

        # Redirect STDOUT
        self.terminal = sys.stdout

        # Set log filename
        global LOGFILE_NAME
        LOGFILE_NAME = logger_output_fname()   # might add unique timestamp

        # Write APPEND to Log
        self.logfile = open(LOGFILE_NAME, mode="a")

    def write(self, msg):

        # Allow colors (if they were set)
        self.terminal.write(msg)

        # Strip off colors (if they were set)
        msg = ui.de_colorize(msg)
        self.logfile.write(msg)
        self.logfile.flush()

    def flush(self):
        pass

def update_status(s):
    """ Update status by writing out (overwriting) a status line """

    fname =  'STATUS-' + gethostname() + '.txt'
    str(s).replace('\n', '; ')
    with open(fname, "w+", encoding='utf-8') as f:  # note that w+ will overwrite the file if it exists, start new file if it does not.
        f.write(s)


# START LOGGER ON IMPORT -----------------------------------------------------------------------------------

sys.stdout = _Logger()
commanline = ' '.join(sys.argv).split('/')[-1]
caption = str(gethostname()).upper() + ': ' + commanline
caption +=  str(str(datetime.now())[:-10]).rjust(ui.WIDTH_CONSOLE-len(caption))
ui.divider('=')
print(caption)
ui.divider('=')

