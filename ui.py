""" User Interface for a Python console. """

import os
import sys
import json
import traceback
from subprocess   import check_output
from   datetime   import datetime


# GLOBALS & CONSTANTS --------------------------------------------------------------------------------------------------
INDENT                 = "        "

try:
    WIDTH_CONSOLE      = int(check_output(['stty', 'size']).split()[1])
except:
    WIDTH_CONSOLE      = 80
WIDTH_PROGBAR          = WIDTH_CONSOLE/2
WIDTH_LOGFILE          = 120
WIDTH_MENU             = WIDTH_CONSOLE/2

NORMAL                 = '\033[0m'
BOLD                   = '\033[1m'
FADE                   = '\033[2m'
ITALIC                 = '\033[3m'
UNDERLINE              = '\033[4m'

COLOR_BLACK            = '\033[90m'
COLOR_RED              = '\033[91m'
COLOR_GREEN            = '\033[92m'
COLOR_YELLOW           = '\033[93m'
COLOR_BLUE             = '\033[94m'
COLOR_MAGENTA          = '\033[95m'
COLOR_CYAN             = '\033[96m'
COLOR_WHITE            = '\033[97m'

HI_WHITE               = '\033[1m\033[9%sm\033[4%sm' % (0, 7)
HI_BLACK               = '\033[1m\033[9%sm\033[4%sm' % (7, 0)
HI_RED                 = '\033[1m\033[9%sm\033[4%sm' % (7, 1)
HI_GREEN               = '\033[1m\033[9%sm\033[4%sm' % (7, 2)
HI_YELLOW              = '\033[1m\033[9%sm\033[4%sm' % (7, 3)
HI_BLUE                = '\033[1m\033[9%sm\033[4%sm' % (7, 4)
HI_MAGENTA             = '\033[1m\033[9%sm\033[4%sm' % (7, 5)
HI_CYAN                = '\033[1m\033[9%sm\033[4%sm' % (7, 6)

# Remove coloring when we are in the cloud - makes log files hard to read
if bool(str(os.uname()[0]) == 'Linux'):

    NORMAL             = ''
    BOLD               = ''
    FADE               = ''
    ITALIC             = ''
    UNDERLINE          = ''
    COLOR_BLACK        = ''
    COLOR_RED          = ''
    COLOR_GREEN        = ''
    COLOR_YELLOW       = ''
    COLOR_BLUE         = ''
    COLOR_MAGENTA      = ''
    COLOR_CYAN         = ''
    COLOR_WHITE        = ''
    HI_WHITE           = ''
    HI_BLACK           = ''
    HI_RED             = ''
    HI_GREEN           = ''
    HI_YELLOW          = ''
    HI_BLUE            = ''
    HI_MAGENTA         = ''
    HI_CYAN            = ''


# FORMATTING -----------------------------------------------------------------------------------------------------------

def colorize(txt, colors):
    """ Apply color to text.
        :param    txt:       text string to be formatted
        :param    colors:    a function, or list of functions, that add color

        :return:  formatted text
    """
    s = txt

    if colors:
        if type(colors) is tuple or type(colors) is list:
            for color in colors:
                if color:
                    s = colorize(s, color)
                s = str(s).replace(NORMAL + NORMAL, NORMAL)
        elif type(colors) is str:
            s = colors + s + NORMAL
        else:
            s = colors(s)
    s = str(s).replace(NORMAL + NORMAL, NORMAL)
    return s

def plaintext(s):


    for FRMT in [ NORMAL, BOLD, FADE, ITALIC, UNDERLINE, COLOR_BLACK, COLOR_RED, COLOR_GREEN,
                  COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE, HI_WHITE, HI_BLACK, HI_RED, HI_GREEN,
                  HI_YELLOW, HI_BLUE, HI_MAGENTA, HI_CYAN,
                  '[40m','[41m','[42m','[43m','[44m','[45m','[46m','[47m' ]:
        try:
            s = str(s).replace(FRMT, '')
        except: pass
    return s


def underline(s):
    return UNDERLINE + s + NORMAL

def italic(s):
    return ITALIC + s + NORMAL

def fade(s):
    return FADE + s + NORMAL

def color_black(s):
    return COLOR_BLACK + s + NORMAL

def color_red(s):
    return COLOR_RED + s + NORMAL

def color_green(s):
    return COLOR_GREEN + s + NORMAL

def color_yellow(s):
    return COLOR_YELLOW + s + NORMAL

def color_blue(s):
    return COLOR_BLUE + s + NORMAL

def color_magenta(s):
    return COLOR_MAGENTA + s + NORMAL

def color_cyan(s):
    return COLOR_CYAN + s + NORMAL

def color_white(s):
    return COLOR_WHITE + s + NORMAL

def hi_black(s):
    return HI_BLACK + s + NORMAL

def hi_red(s):
    return HI_RED + s + NORMAL

def hi_green(s):
    return HI_GREEN + s + NORMAL

def hi_yellow(s):
    return HI_YELLOW + s + NORMAL

def hi_blue(s):
    return HI_BLUE + s + NORMAL

def hi_magenta(s):
    return HI_MAGENTA + s + NORMAL

def hi_cyan(s):
    return HI_CYAN + s + NORMAL

def hi_white(s):
    return HI_WHITE + s + NORMAL


# MENUS ----------------------------------------------------------------------------------------------------------------

def menu(options, title=None, default=None, shortcuts=False, simplelist=True):

    def is_number(s):
        try:
            float(s)
        except:
            return False
        else:
            return True

    try:
        selection = None

        # Edit the title, adding the default option if necessary.
        if not title or not str(title).strip():
            title = str('Select an option: ')
        else:
            title = str(title).strip()
            title = title + ': ' if not title.endswith(':') else title + ' '
        title = title[:-2] + ' [' + str(default) + ']: ' if default else title
        title = UNDERLINE + title + NORMAL

        # Convert simple list to a list of tuples if the simplelist flag is set.
        options = [ (optno + 1, options[optno])
                    for optno in range(len(options))] if simplelist else options

        # Find max width of the menu
        colwidth = 10
        for opt in options:
            if len(str(opt[1])) > colwidth: colwidth = len(str(opt[1]))
        colwidth += 2

        # Make sure we start with a clean console line
        sys.stdout.write('\r'.ljust(WIDTH_CONSOLE))
        sys.stdout.write('\r')
        sys.stdout.flush()

        # display
        print()
        print(title)
        lineno = 0
        for opt in options:
            if str(opt[1]).startswith('\n'): print()  # insert blankline?
            lineno += 1
            linestr = ' ' + str(str(lineno) + '.').ljust(4, ' ')
            linestr += str(opt[1]).ljust(colwidth)
            if len(opt) > 2: linestr += '\t' + str(opt[2])
            print(linestr)

        print()

        # get choice
        try:
            choice = input(' Select:  ' + NORMAL)
        except (KeyboardInterrupt, SystemExit):
            print()
            raise
        except:
            return None

        # validate choice
        if choice and not shortcuts and not is_number(choice):
            print('Invalid selection')
            return None

        # determine choice
        if choice == '' and default:
            sys.stdout.write('\033[1A')  # go up a line
            sys.stdout.flush()
            print(NORMAL + '\r Select:  ' + str(default) + NORMAL)
            print()
            return default

        # determine choice
        if choice == '':     return None
        elif choice is None: return None
        elif is_number(choice):
            choice = int(choice) - 1  # return to base zero
        elif shortcuts and len(choice) == 1:
            choice = str(choice).upper()
            for index in range(len(options)):
                option = options[index][1]

                # check each char in option, and check first capitalized one
                for char in option:
                    if char == str(char).upper():
                        if choice == char:
                            choice = index
                        break
                if is_number(choice): break
        else: return None

        # determine selection
        if is_number(choice):
            if int(choice) < len(options):
                if options[choice] is not None:
                    if simplelist:
                        selection = options[choice][1]
                    else:
                        selection = options[choice][0]
            else:
                print('Invalid selection...')
                return

        if selection: print()
        return selection

    except (KeyboardInterrupt, SystemExit): raise
    except Exception as e: print('ERROR', e)

def ask(prompt, default=None, force_int=False):

    def is_number(s):
        try:
            float(s)
        except:
            return False
        else:
            return True

    try:
        prompt = str(prompt).strip()
        if not prompt.endswith(':'): prompt += ':'
        prompt += ' '
        if default: prompt = prompt[:-2] + ' [' + str(default) + ']: '
        entry = input(prompt )
        if not entry:
            if default: entry = default
            else:       entry = None
        else:
            entry = str(entry).strip()
        if force_int:
            if is_number(entry): entry = int(entry)
            else: entry = None
        return entry
    except (KeyboardInterrupt, SystemExit):
        print()
        raise
    except:
        return None

def confirm(prompt='OK to continue? ', default=True):
    try:
        prompt = str(prompt).strip()
        prompt = prompt.strip()
        if default: prompt += ' [Y/n]: '
        else: prompt += ' [y/N]: '
        choice = input(prompt)
        if choice:
            choice = str(choice).upper()
            if choice == 'Y':
                return True
            else:
                return False
        else:
            return default
    except (KeyboardInterrupt, SystemExit):
        print()
        raise
    except: return default


# PROGBAR --------------------------------------------------------------------------------------------------------------

def progbar(x, msg='', width=50):
    """ Display progbar where x is ratio completed (e.g.,  x=.477 becomes 48%) """

    try:
        if x > 1.0:
            x = 1.0
        x = float(x) * 100
        w = min(100, width - 9)
        p = min(100, int(-(-float(x * w) // float(100))))  # Note trick to implement math.ceil
        sys.stdout.write('\r' + msg + '  ' +
                         str(' ' + str("%.1f" % round(x, 1)).rjust(4, ' ') + '%').ljust(7) +
                         ' [' + '#' * p + '-' * (w - p) + ']')
        if x >= 100: sys.stdout.write('\n')
        sys.stdout.flush()
    except Exception as e:
        print(e)


# CONSOLE MESSAGING ----------------------------------------------------------------------------------------------------

def banner(txt=' ', colors=(color_white, hi_blue), width=None, stamp_time=True):
    """Print message as a banner"""
    if not width: width = console_width()
    if stamp_time: txt +=  str(str(datetime.now())[:-10]).rjust(width - len(txt))
    if not colors or bool(str(os.uname()[0]) == 'Linux'):
        divider(width=width)
        print(txt)
        divider(width=width)
    else:
        print(colorize(txt.ljust(console_width()), colors))

def section(txt, capitalize=True):
    """Print message as a sub-HEADER"""
    if capitalize: txt = str(txt).upper()
    print()
    print(' >', txt)
    print()

def divider(char='-', width=None):
    if not width: width = console_width()
    print(char * width)

def message(msg, prefix='', warning=False, err=False, ljust=False, fcolor=COLOR_BLUE, bcolor='', lf=True, tracebk=False):

    # Handle Tracebacks
    if tracebk is True:
        tracebk = traceback.format_exc()

    # Handle Exceptions
    if msg is Exception:
        msg = str(msg).strip().upper()
        err = True
        if not tracebk: tracebk = traceback.format_exc()

    # Handle Objects
    if type(msg) is not str and type(msg) is not Exception:
        try:
            msg = json.dumps(msg)  # convert obj to string
        except:
            try: msg = str(msg)
            except: msg = 'Cannot log - invalid msg'

    # Remove newline at start of a line
    if str(msg).startswith('\n'):
        msg = msg[1:]

    # Add prefix
    if prefix:
        msg = prefix + msg

    # Handle warnings
    if warning:
        msg = str(msg).replace('\n', ';  ') # flatten to one line

    # Print out the msg
    try:

        # Errors
        if err:
            print()
            print(HI_RED + str('ERROR: ' + msg).ljust(WIDTH_CONSOLE) + NORMAL)
            if tracebk:
                lines = str(tracebk).strip().split('\n')
                out   = []

                if lines:
                    try:

                        for line in lines[1:-1]:
                            line = str(line).strip()
                            if str(line).startswith('File '):
                                out.append(line)
                            else:
                                if out: out[-1] = out[-1] + ':  ' + line
                                else:   out.append(line)
                        if out:
                            for line in out:
                                print(COLOR_RED + line + NORMAL)
                    except Exception as e: print('TRACEBACK ERROR:', str(e))
            print()

       # Non-Errors
        else:

            if bcolor: msg = str(bcolor) + msg.ljust(WIDTH_CONSOLE)
            if warning:   msg = COLOR_RED + BOLD + msg

            msg = '    ' + COLOR_WHITE + msg

            if ljust:  msg = str(msg).ljust(WIDTH_CONSOLE - 24)

            if lf:
                print(fcolor + msg + NORMAL)
            else:
                print(fcolor + msg + NORMAL, end='', flush=True)

    except Exception as e:
        try:
            print('CONSOLE ERROR:', str(e))
            print('ORIGINAL TEXT:', str(msg))
            traceback.print_exc()
        except: pass

def count(num, description='', col_width=20):
    """Print an aligned numerical count and a description"""
    if num is None:
        num = ''
    elif str(num).isnumeric():
        num = "{:,}".format(num).rjust(col_width)
    else:
        num = str(num).rjust(col_width)
    print(num + '  ' + str(description).rstrip())

def warn(msg):
    msg(msg, warning=True)

def alert(e=None, tracebk=True):
    if not e:
        tracebk = True
    message(e, err=True, tracebk=tracebk)

def debug(msg, verbose=False):

    # Only print out debugging lineitems when program was called
    if verbose or 'debug' in [str(flag).lower() for flag in sys.argv]:
        msg(msg, prefix='>>>>>>> ')

def clear():
    os.system('clear')

def console_width():
    try:
        return int(check_output(['stty', 'size']).split()[1])
    except:
        return 80