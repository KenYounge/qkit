""" Debug custom data structures, object sizes, and memory issues. """

import os
import sys
import csv
import psutil
from   random      import shuffle as random_shuffle
from   numbers     import Number
from   collections import Set, Mapping, deque

def view_dct(dct, fname='', n_rows=100):
    fname = str(fname.strip())
    if not fname.endswith('.csv'): fname += '.csv'
    if n_rows > len(dct): n_rows = len(dct)
    if os.path.exists(fname): os.remove(fname)
    if fname:
        with open(fname, 'w') as f:
            writer = csv.writer(f, dialect='excel')
            keys = list(dct.keys())
            random_shuffle(keys)
            for key in keys[:n_rows]:
                writer.writerow( (key, dct[key]))
    else:
        print()
        print('DEBUG: ' + fname)
        print()
        keys = list(dct.keys())
        for key in keys[:n_rows]:
            print((key, dct[key]))

def view_lst(lst, fname='', n_rows=100):
    if n_rows > len(lst): n_rows = len(lst)
    fname = str(fname.strip())
    if not fname.endswith('.csv'): fname += '.csv'
    indices = list(range(len(lst)))
    random_shuffle(indices)
    if os.path.exists(fname): os.remove(fname)
    if fname:
        with open(fname, 'w') as f:
            for i in indices[:n_rows]:
                item = str(lst[i])
                if i < (len(lst) - 1): item += "\n"
                f.write(item)
    else:
        print()
        print('DEBUG: ' + fname)
        print()
        for i in indices[:n_rows]:
            item = str(lst[i])
            print(item)

def view_set(s, fname='', n_rows=100):
    lst = list(s)
    view_lst(lst, fname=fname, n_rows=n_rows)

def view_memory():
    print(psutil.virtual_memory())

def view_size(obj_0):
    """ Recursively iterate to sum size of object & members. Source: https://stackoverflow.com/questions/449560/ """
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'
    _seen_ids = set()
    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

def view_head(x, name='', num_rows=5):
    """Print the top header of rows of an object"""
    if type(x) is dict:
        print(name, dict(list(x.items())[0:num_rows]))
    elif type(x) is set:
        print(name, set([item for item in list(x)[0:num_rows]]))
    else:
        print(name, x[0:num_rows])

def view_docstring(docstring, program):
    print()
    print(str(program).upper())
    print()
    print(docstring)
    print()
    print('-' * 40)
    print()

