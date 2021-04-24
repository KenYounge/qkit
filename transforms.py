""" Numerical Transformations """

import random
from   math       import exp
from   numpy      import cumsum as np_cumsum

def argmax_proba(values):
    """ Return probabilies w/r/t the max value, scaled to the number of max values """

    # Handle special cases
    if len(values) == 1:
        return [1,]

    probs     = []
    max_value = max(values)
    flag_max  = [i == max_value for i in values]
    num_maxes = sum(flag_max)

    for i in flag_max:
        if i:
            probs.append(1 / num_maxes)
        else:
            probs.append(0)
    return probs

def softmax_proba(values, tau):
    """ Return probabilites for each value, scaled by the magnitude of the value and the softmax temperature (the hyper-parameter tau) """

    # Special case: only one option
    if len(values) == 1:
        return [1,]

    # Special case: if Tau very small, that is the argmax
    if tau < 0.0001:
        return argmax_proba(values)

    # Replace none values with min
    for i in range(len(values)):
        if values[i] is None:
            values[i] = 0

    # Calc softmax probabilities
    try:
        scaled = [v/tau for v in values]
        denom  = sum([exp(v) for v in scaled])
        probs  = [exp(v)/denom for v in scaled]
        return probs

    # ERR: Divide by zero:  Tau is too small, that is the argmax
    except ZeroDivisionError:
        return argmax_proba(values)

    # ERR: Overflow: Tau too small or exp(v) too large, again use argmax
    except OverflowError:
        return argmax_proba(values)

    except Exception as e:
        raise e

def softmax_select_idx(values, tau):
    """ Select an index into values based on making a softmax selection """
    splits = np_cumsum(softmax_proba(values, tau))
    p = random.random()
    for i in range(len(splits)):
        if p < splits[i]:
            return i
    return len(splits)-1

def sigmoid_across_unit_interval(p, k=1.2):
    """ Sigmoid transformation for a unit interval.

            Returns: a value [0,1] associated with a proportion [0,1]

            Parameters:

                p -- proportion across the unit interval [0,1]
                k -- shape of the simoid transformation

            Special return values based on k:

               if k==  0      then always return 0
               if 0 < k < 1   then always return 1

            For all continuous values for k >= 1.0

                1.0  step function with a sharp setup from 0 to 1 in the middle at p = 0.5
                1.1  very steep transition in the middle at p = 0.5
                1.2  transition looks much like a default logistic transition
                1.3  transition flattens, becoming more linear as k increases
                ...
                2.0  transition is almost linear by k = 2.0

            Source:

                Function inspired by suggestions made here:
                https://dinodini.wordpress.com/2010/04/05/normalized-tunable-sigmoid-functions/
    """
    assert p >= 0, 'Custom sigmoid function has a domain of [0,1]'
    assert p <= 1, 'Custom sigmoid function has a domain of [0,1]'
    assert k >= 0, 'Shaping parameter must always be > = 0'

    k = float(k)

    if k < 0.0000000001 : return 0   # special case
    if k < 1.0          : return 1   # special case

    p = (p * 2) - 1

    if not p: return 0.5  # undefined at inflection point
    if p < 0: return 0.5 + ((-k * p) / (-k + p + 1)) * .5
    else:     return 0.5 + ((-k * p) / (-k - p + 1)) * .5

def decay_across_unit_interval(v, p, d):
    """ Generalized decay function over unit interval.

            Returns: initial value rescaled based on decay factor

            Parameters:

                v:         Starting value
                p:         Percent completed    must be in a unit interval [0,1]
                d:         Decay trajectory     must be in a unit interval [0,1]

            Example values for d:

                d = 0.00   No decay             return starting value
                d = 0.25   Slow onset           decay slowly and then accelerate
                d = 0.50   Linear decay         45 degree) decay across interval
                d = 0.75   Fast onset           decay fast and then deccelerate
                d = 1.00   Immediate decay      return

            Author:  KenYounge@gmail.com
            License: GNU General Public License with attribution
    """

    # No decay
    if d == 0.0:
        return v

    # Slow onset
    if d <= 0.5:
        return v * (1 - p ** (1.0 / (d * 2)))

    # Linear decay
    if d == 0.5:
        return v * (1 - p)

    # Fast onset
    if d  > 0.5:
        return v * ( decay_across_unit_interval(1, p, 0.5)
                     - (decay_across_unit_interval(1, 1 - p, 1 - d)
                        - decay_across_unit_interval(1, 1 - p, 0.5))
                   )

    # Immediate decay
    if d == 1.0: return 0

def average_lists_by_idx(lists):
    """ Return a new list with column-by-column average calculated across all other lists. """
    return [float(sum(col))/len(col) for col in zip(*lists)]

def percentile_lists_by_idx(lists, pctile, max_len):
    """ Return a new list with column-by-column percentile calculated across other lists. """

    data    = [ list() for _ in range(max_len)]
    pctiles = list()

    # reshape lists so they align by move
    for lst in lists:
        for i in range(max_len):
            if i < len(lst):
                data[i].append(lst[i])

    for i in range(max_len):
        curlist = sorted(data[i])
        if len(curlist) > 0:
            cut = int(len(curlist) * float(pctile))
            if cut > len(curlist)-1:
                cut = len(curlist)-1
            if cut == -1: cut = 0
            assert cut >= 0
            assert cut < len(curlist)
            pctiles.append(curlist[cut])
    return pctiles
