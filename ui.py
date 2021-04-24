""" Utilities for a Python console """

import os
import sys
import json
import traceback


# GLOBALS --------------------------------------------------------------------

DEBUG                  = 'debug' in [str(flag).lower() for flag in sys.argv]
CLOUD                  =  bool(str(os.uname()[0]) == 'Linux')  # Linux implies cloud


# CONSTANTS --------------------------------------------------------------------

WIDTH_PROGBAR          = 50
WIDTH_CONSOLE          = 80
WIDTH_LOGFILE          = 120
WIDTH_MENU_BAR         = 40

INDENT                 = "        "
INDENT_ERR_DETAIL      = '              '

# COLORS

TXT_NORMAL             = '\033[0m'
TXT_BOLD               = '\033[1m'
TXT_FAINT              = '\033[2m'
TXT_ITALIC             = '\033[3m'
TXT_UNDERLINE          = '\033[4m'
TXT_BLACK              = '\033[90m'
TXT_RED                = '\033[91m'
TXT_GREEN              = '\033[92m'
TXT_YELLOW             = '\033[93m'
TXT_BLUE               = '\033[94m'
TXT_MAGENTA            = '\033[95m'
TXT_CYAN               = '\033[96m'
TXT_WHITE              = '\033[97m'

HI_WHITE               = '\033[1m\033[9%sm\033[4%sm' % (0, 7)
HI_BLACK               = '\033[1m\033[9%sm\033[4%sm' % (7, 0)
HI_RED                 = '\033[1m\033[9%sm\033[4%sm' % (7, 1)
HI_GREEN               = '\033[1m\033[9%sm\033[4%sm' % (7, 2)
HI_YELLOW              = '\033[1m\033[9%sm\033[4%sm' % (7, 3)
HI_BLUE                = '\033[1m\033[9%sm\033[4%sm' % (7, 4)
HI_MAGENTA             = '\033[1m\033[9%sm\033[4%sm' % (7, 5)
HI_CYAN                = '\033[1m\033[9%sm\033[4%sm' % (7, 6)

def turn_colors_off():

    global TXT_NORMAL
    global TXT_BOLD
    global TXT_FAINT
    global TXT_ITALIC
    global TXT_UNDERLINE
    global TXT_BLACK
    global TXT_RED
    global TXT_GREEN
    global TXT_YELLOW
    global TXT_BLUE
    global TXT_MAGENTA
    global TXT_CYAN
    global TXT_WHITE
    global HI_WHITE
    global HI_BLACK
    global HI_RED
    global HI_GREEN
    global HI_YELLOW
    global HI_BLUE
    global HI_MAGENTA
    global HI_CYAN

    TXT_NORMAL             = ''
    TXT_BOLD               = ''
    TXT_FAINT              = ''
    TXT_ITALIC             = ''
    TXT_UNDERLINE          = ''
    TXT_BLACK              = ''
    TXT_RED                = ''
    TXT_GREEN              = ''
    TXT_YELLOW             = ''
    TXT_BLUE               = ''
    TXT_MAGENTA            = ''
    TXT_CYAN               = ''
    TXT_WHITE              = ''
    HI_WHITE               = ''
    HI_BLACK               = ''
    HI_RED                 = ''
    HI_GREEN               = ''
    HI_YELLOW              = ''
    HI_BLUE                = ''
    HI_MAGENTA             = ''
    HI_CYAN                = ''

# COLORS -----------------------------------------------------------------------

def black(s):        return TXT_BLACK   + s + TXT_NORMAL
def red(s):          return TXT_RED     + s + TXT_NORMAL
def green(s):        return TXT_GREEN   + s + TXT_NORMAL
def yellow(s):       return TXT_YELLOW  + s + TXT_NORMAL
def blue(s):         return TXT_BLUE    + s + TXT_NORMAL
def magenta(s):      return TXT_MAGENTA + s + TXT_NORMAL
def cyan(s):         return TXT_CYAN    + s + TXT_NORMAL
def white(s):        return TXT_WHITE   + s + TXT_NORMAL

def black_highlight(s):    return HI_BLACK    + s + TXT_NORMAL
def red_highlight(s):      return HI_RED      + s + TXT_NORMAL
def green_highlight(s):    return HI_GREEN    + s + TXT_NORMAL
def yellow_highlight(s):   return HI_YELLOW   + s + TXT_NORMAL
def blue_highlight(s):     return HI_BLUE     + s + TXT_NORMAL
def magenta_highlight(s):  return HI_MAGENTA  + s + TXT_NORMAL
def cyan_highlight(s):     return HI_CYAN     + s + TXT_NORMAL
def white_highlight(s):    return HI_WHITE    + s + TXT_NORMAL

def underline(s):  return TXT_UNDERLINE + s + TXT_NORMAL


# METHODS ------------------------------------------------------------------------

def colorize(txt, colors):
    """ Apply color format codes to text.
        :param    txt:       string to be formatted
        :param    colors:    function, or list of functions, that add color

        :return:  formatted text
    """
    s = txt

    if colors:
        if type(colors) is tuple or type(colors) is list:
            for color in colors:
                if color:
                    s = color(s)
                s = str(s).replace(TXT_NORMAL + TXT_NORMAL, TXT_NORMAL)
        else:
            s = colors(s)
    return s

def de_colorize(s):
    s = str(s).replace(TXT_BOLD, '')
    s = str(s).replace(TXT_FAINT, '')
    s = str(s).replace(TXT_ITALIC, '')
    s = str(s).replace(TXT_UNDERLINE, '')
    s = str(s).replace(TXT_BLACK, '')
    s = str(s).replace(TXT_RED, '')
    s = str(s).replace(TXT_GREEN, '')
    s = str(s).replace(TXT_YELLOW, '')
    s = str(s).replace(TXT_BLUE, '')
    s = str(s).replace(TXT_MAGENTA, '')
    s = str(s).replace(TXT_CYAN, '')
    s = str(s).replace(TXT_WHITE, '')
    s = str(s).replace(HI_WHITE, '')
    s = str(s).replace(HI_BLACK, '')
    s = str(s).replace(HI_RED, '')
    s = str(s).replace(HI_GREEN, '')
    s = str(s).replace(HI_YELLOW, '')
    s = str(s).replace(HI_BLUE, '')
    s = str(s).replace(HI_MAGENTA, '')
    s = str(s).replace(HI_CYAN, '')
    s = str(s).replace(TXT_NORMAL, '')
    s = str(s).replace('[40m', '')
    s = str(s).replace('[41m', '')
    s = str(s).replace('[42m', '')
    s = str(s).replace('[43m', '')
    s = str(s).replace('[44m', '')
    s = str(s).replace('[45m', '')
    s = str(s).replace('[46m', '')
    s = str(s).replace('[47m', '')
    return s

def clear_terminal():
    os.system('clear')

def divider(char='-'):
    print(char * WIDTH_CONSOLE)

def banner(msg=' ', colors=(white, blue_highlight)):
    print(colorize(msg.ljust(WIDTH_CONSOLE), colors))


# MENU ------------------------------------------------------------------------

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
        title = TXT_UNDERLINE + title + TXT_NORMAL

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
            choice = input(' Select:  ' + TXT_NORMAL)
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
            print(TXT_NORMAL + '\r Select:  ' + str(default) + TXT_NORMAL)
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


# PROGBAR ----------------------------------------------------------------------

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


# PRINT MESSAGES ---------------------------------------------------------------

def info(msg, prefix='', warning=False, err=False, ljust=False, fcolor=TXT_BLUE, bcolor='', lf=True, tracebk=False):

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

    # Log the msg
    try:

        # Errors
        if err:
            print()
            print(HI_RED + str('ERROR: ' + msg).ljust(WIDTH_CONSOLE) + TXT_NORMAL)
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
                                print(TXT_RED + line + TXT_NORMAL)
                    except Exception as e: print('TRACEBACK ERROR:', str(e))
            print()

       # Non-Errors
        else:

            if bcolor: msg = str(bcolor) + msg.ljust(WIDTH_CONSOLE)
            if warning:   msg = TXT_RED + TXT_BOLD + msg

            msg = '    ' + TXT_WHITE + msg

            if ljust:  msg = str(msg).ljust(WIDTH_CONSOLE - 24)

            if lf:
                print(fcolor  + msg + TXT_NORMAL)
            else:
                print(fcolor  + msg + TXT_NORMAL, end='', flush=True)

    except Exception as e:
        try:
            print('CONSOLE ERROR:', str(e))
            print('ORIGINAL TEXT:', str(msg))
            traceback.print_exc()
        except: pass

def warn(msg):
    info(msg, warning=True)

def error(e=None, tracebk=True):
    if not e:
        tracebk = True
    info(e, err=True, tracebk=tracebk)

def debug(msg):
    if DEBUG:
        info(msg, prefix='>>>>>>> ' )
