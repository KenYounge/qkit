""" Utilities """

import sys
import subprocess
import time
import datetime

from   sys        import argv
from   os         import uname
from   socket     import gethostname
from   random     import randint as random_randint
from   datetime   import datetime

def in_debug():
    return 'debug' in [str(flag).lower() for flag in argv]

def in_cloud():
    return bool(str(uname()[0]) == 'Linux')  # Linux implies cloud

def in_jupyter():
    try:
        return 'ipykernel' in sys.modules
    except:
        return False

def is_number(s):
    try:    float(s)
    except: return False
    else:   return True

def flags(value):
    """Return a list of the set binary flags. For example:  [2, 16, 64]  """
    flags = []
    while value:
        _current_bit = value & (~value+1)
        flags.append(_current_bit)
        value ^= _current_bit
    return flags

def host_name():
    return gethostname()

def git_version():
    return str(subprocess.check_output('git rev-parse --short HEAD', shell=True)).strip()

def date_stamp():
    return str(datetime.date.today())

def time_stamp():
    return str(time.strftime("%m/%d %H:%M", time.localtime(time.time())))

def time_stamp_id():
    ts = str(str(datetime.now())[:-10]).replace(' ','-').replace(':','-')
    ts = ts[:10] + '_' + ts[11:] + '_' + make_an_id()
    return ts

def make_an_id():
    return str(hex(int((time.time()*10000000)/float(random_randint(1,10000000))))[2:])

def format_value(val, digits=2, min_val=None, supress_zero=False):
    if val is None: return ''
    if val == '': return ''
    if min_val is not None and val <= min_val:
        return '.'
    if digits is None: digits = 2
    mask = "%0." + str(digits) + "f"
    if supress_zero and abs(val) < (1 / (10 ** digits) ):
        return ' '
    elif val >= 0:
        return ' ' + str(mask % val)
    else:
        return str(mask % val)

def validate_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return date_string + ' 00:00:00'
    except ValueError:
        return ''

def validate_string(raw_string):
    try:
        if raw_string == 'NULL':
            return ''
        else:
            return raw_string
    except ValueError:
        return ''

def parse_iso8601tz(date_string):
    """return a datetime object for a string in ISO 8601 format.

    This function parses strings in exactly this format:
    '2012-12-26T13:31:47.823-08:00'

    Sadly, datetime.strptime's %z format is unavailable on many platforms,
    so we can't use a single strptime() call.
    """

    dt = datetime.datetime.strptime(date_string[:-6],
                                    '%Y-%m-%dT%H:%M:%S.%f')

    # parse the timezone offset separately
    delta = datetime.timedelta(minutes=int(date_string[-2:]),
                               hours=int(date_string[-5:-3]))
    if date_string[-6] == '-':
        # add the delta to return to UTC time
        dt = dt + delta
    else:
        dt = dt - delta
    return dt

def split_list(lst, num_lists_returned):
    original_length = len(lst)
    return [lst[i * original_length // num_lists_returned: (i + 1) * original_length // num_lists_returned]
            for i in range(num_lists_returned)]

def batch_iterable(iterable, batch_size=1):
    """Break an iterable into batches."""
    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx+batch_size, l)]

def batch_break_points(lst, batch_no, num_batches):
    assert batch_no < num_batches
    assert num_batches < len(lst)
    batch_size = int(len(lst)/num_batches) + 1
    idx_start  = batch_no * batch_size
    idx_stop   = (batch_no + 1) * batch_size
    if idx_stop > len(lst): idx_stop = len(lst)  # possibly cut short final batch
    return idx_start, idx_stop
