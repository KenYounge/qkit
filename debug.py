""" Debug utilities to view data structures, memory, etc.  """

import os
import sys
import csv
import psutil
from   random      import shuffle as random_shuffle
from   numbers     import Number
from   collections import Set, Mapping, deque

def debug_dct(dct, fname='', n_rows=100):
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

def debug_lst(lst, fname='', n_rows=100):
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

def debug_set(s, fname='', n_rows=100):
    lst = list(s)
    debug_lst(lst, fname=fname, n_rows=n_rows)

def debug_memory():
    print(psutil.virtual_memory())

def debug_size(obj_0):
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