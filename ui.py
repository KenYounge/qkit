""" User Interface for a Python console. """

import os
import sys
import json
import traceback
from   subprocess      import check_output
from   datetime        import datetime

# FORMAT CONSTANTS -----------------------------------------------------------------------------------------------------

class Formats:

    NORMAL           = '\033[0m'
    BOLD             = '\033[1m'
    FADE             = '\033[2m'
    ITALIC           = '\033[3m'
    UNDERLINE        = '\033[4m'

    BLACK            = '\033[90m'
    RED              = '\033[91m'
    GREEN            = '\033[92m'
    YELLOW           = '\033[93m'
    BLUE             = '\033[94m'
    MAGENTA          = '\033[95m'
    CYAN             = '\033[96m'
    WHITE            = '\033[97m'

    WHITE_H          = '\033[1m\033[9%sm\033[4%sm' % (0, 7)
    BLACK_H          = '\033[1m\033[9%sm\033[4%sm' % (7, 0)
    HI_RED           = '\033[1m\033[9%sm\033[4%sm' % (7, 1)
    GREEN_H          = '\033[1m\033[9%sm\033[4%sm' % (7, 2)
    YELLOW_H         = '\033[1m\033[9%sm\033[4%sm' % (7, 3)
    BLUE_H           = '\033[1m\033[9%sm\033[4%sm' % (7, 4)
    MAGENTA_H        = '\033[1m\033[9%sm\033[4%sm' % (7, 5)
    CYAN_H           = '\033[1m\033[9%sm\033[4%sm' % (7, 6)


# GLOBALS  -------------------------------------------------------------------------------------------------------------

F = Formats()
W = 80
I = " " * 8


# FORMAT FUNCTIONS -----------------------------------------------------------------------------------------------------

def clear_screen():
    os.system('clear')

def get_width():
    """ Refresh global width variable """
    global W
    try:
        W = int(check_output(['stty', 'size']).split()[1])
    except:
        W = 80
    return W

def stop_coloring():

    global F

    F.NORMAL = ''
    F.BOLD = ''
    F.FADE = ''
    F.ITALIC = ''
    F.UNDERLINE = ''
    F.BLACK = ''
    F.RED = ''
    F.GREEN = ''
    F.YELLOW = ''
    F.BLUE = ''
    F.MAGENTA = ''
    F.CYAN = ''
    F.WHITE = ''
    F.WHITE_H = ''
    F.BLACK_H = ''
    F.HI_RED = ''
    F.GREEN_H = ''
    F.YELLOW_H = ''
    F.BLUE_H = ''
    F.MAGENTA_H = ''
    F.CYAN_H = ''

def style(txt, colors):
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
                    s = style(s, color)
                s = str(s).replace(F.NORMAL + F.NORMAL, F.NORMAL)
        elif type(colors) is str:
            s = colors + s + F.NORMAL
        else:
            s = colors(s)
    s = str(s).replace(F.NORMAL + F.NORMAL, F.NORMAL)
    return s

def strip_formatting(s):

    for FRMT in [ F.NORMAL, F.BOLD, F.FADE, F.ITALIC, F.UNDERLINE, F.BLACK, F.RED, F.GREEN,
                  F.YELLOW, F.BLUE, F.MAGENTA, F.CYAN, F.WHITE, F.WHITE_H, F.BLACK_H, F.HI_RED, F.GREEN_H,
                  F.YELLOW_H, F.BLUE_H, F.MAGENTA_H, F.CYAN_H, '[40m','[41m','[42m','[43m','[44m','[45m','[46m','[47m' ]:
        try:
            return str(s).replace(FRMT, '')
        except:
            return s

def underline(s):
    return F.UNDERLINE + s + F.NORMAL

def italic(s):
    return F.ITALIC + s + F.NORMAL

def fade(s):
    return F.FADE + s + F.NORMAL

def black(s):
    return F.BLACK + s + F.NORMAL

def black_h(s):
    return F.BLACK_H + s + F.NORMAL

def white(s):
    return F.WHITE + s + F.NORMAL

def white_h(s):
    return F.WHITE_H + s + F.NORMAL

def red(s):
    return F.RED + s + F.NORMAL

def red_h(s):
    return F.HI_RED + s + F.NORMAL

def green(s):
    return F.GREEN + s + F.NORMAL

def green_h(s):
    return F.GREEN_H + s + F.NORMAL

def blue(s):
    return F.BLUE + s + F.NORMAL

def blue_h(s):
    return F.BLUE_H + s + F.NORMAL

def yellow(s):
    return F.YELLOW + s + F.NORMAL

def yellow_h(s):
    return F.YELLOW_H + s + F.NORMAL

def magenta(s):
    return F.MAGENTA + s + F.NORMAL

def magenta_h(s):
    return F.MAGENTA_H + s + F.NORMAL

def cyan(s):
    return F.CYAN + s + F.NORMAL

def cyan_h(s):
    return F.CYAN_H + s + F.NORMAL


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
        title = F.UNDERLINE + title + F.NORMAL

        # Convert simple list to a list of tuples if the simplelist flag is set.
        options = [ (optno + 1, options[optno])
                    for optno in range(len(options))] if simplelist else options

        # Find max width of the menu
        colwidth = 10
        for opt in options:
            if len(str(opt[1])) > colwidth: colwidth = len(str(opt[1]))
        colwidth += 2

        # Make sure we start with a clean console line
        sys.stdout.write('\r'.ljust(W))
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
            choice = input(' Select:  ' + F.NORMAL)
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
            print(F.NORMAL + '\r Select:  ' + str(default) + F.NORMAL)
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


# MESSAGING ------------------------------------------------------------------------------------------------------------

def banner(txt=' ', colors=(white, blue_h), width=W, stamp_time=True):
    """Print message as a banner"""
    if stamp_time: txt +=  str(str(datetime.now())[:-10]).rjust(width - len(txt))
    if not colors or bool(str(os.uname()[0]) == 'Linux'):
        divider(width=width)
        print(txt)
        divider(width=width)
    else:
        print(style(txt.ljust(W), colors))

def section(txt, capitalize=True):
    """Print message as a sub-HEADER"""
    if capitalize: txt = str(txt).upper()
    print()
    print(' >', txt)
    print()

def divider(char='-', width=W):
    print(char * width)

def message(msg, prefix='', warning=False, err=False, ljust=False, fcolor=F.BLUE, bcolor='', lf=True, tracebk=False):

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
            print(F.HI_RED + str('ERROR: ' + msg).ljust(W) + F.NORMAL)
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
                                print(F.RED + line + F.NORMAL)
                    except Exception as e: print('TRACEBACK ERROR:', str(e))
            print()

       # Non-Errors
        else:

            if bcolor: msg = str(bcolor) + msg.ljust(W)
            if warning:   msg = F.RED + F.BOLD + msg

            msg = '    ' + F.WHITE + msg

            if ljust:  msg = str(msg).ljust(W - 24)

            if lf:
                print(fcolor + msg + F.NORMAL)
            else:
                print(fcolor + msg + F.NORMAL, end='', flush=True)

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

