#problem-set-03

# no other imports needed
from collections import defaultdict
import math
#

### PART 1: SEARCHING UNSORTED LISTS

# search an unordered list L for a key x using iterate
def isearch(L, x):
    return iterate(lambda found, item: found or item == x, False, L)

def iterate(f, x, a):
    # done. do not change me.
    if len(a) == 0:
        return x
    else:
        return iterate(f, f(x, a[0]), a[1:])

# search an unordered list L for a key x using reduce
def rsearch(L, x):
    matches = [item == x for item in L]
    return reduce(lambda a, b: a or b, False, matches)

def reduce(f, id_, a):
    # done. do not change me.
    if len(a) == 0:
        return id_
    elif len(a) == 1:
        return a[0]
    else:
        # can call these in parallel
        res = f(reduce(f, id_, a[:len(a)//2]),
                 reduce(f, id_, a[len(a)//2:]))
        return res

def ureduce(f, id_, a):
    if len(a) == 0:
        return id_
    elif len(a) == 1:
        return a[0]
    else:
        # can call these in parallel
        return f(reduce(f, id_, a[:len(a)//3]),
                 reduce(f, id_, a[len(a)//3:]))

### PART 3: PARENTHESES MATCHING

def plus(x, y):
    # done. do not change me.
    return x + y

#### Iterative solution
def parens_match_iterative(mylist):
    return iterate(parens_update, 0, mylist) == 0

def parens_update(current_output, next_input):
    # Once the sequence becomes invalid, keep it invalid
    if current_output < 0:
        return current_output

    if next_input == '(':
        return current_output + 1
    elif next_input == ')':
        return current_output - 1
    else:
        return current_output

#### Scan solution

def parens_match_scan(mylist):
    mapped = list(map(paren_map, mylist))
    prefix_sums, total = scan(plus, 0, mapped)

    min_prefix = reduce(min_f, 0, prefix_sums)

    return total == 0 and min_prefix >= 0

def scan(f, id_, a):
    """
    This is a horribly inefficient implementation of scan
    only to understand what it does.
    We saw a more efficient version in class. You can assume
    the more efficient version is used for analyzing work/span.
    """
    return (
            [reduce(f, id_, a[:i+1]) for i in range(len(a))],
             reduce(f, id_, a)
           )

def paren_map(x):
    """
    Returns 1 if input is '(', -1 if ')', 0 otherwise.
    This will be used by your `parens_match_scan` function.
    
    Params:
       x....an element of the input to the parens match problem (e.g., '(' or 'a')
       
    >>>paren_map('(')
    1
    >>>paren_map(')')
    -1
    >>>paren_map('a')
    0
    """
    if x == '(':
        return 1
    elif x == ')':
        return -1
    else:
        return 0

def min_f(x,y):
    """
    Returns the min of x and y. Useful for `parens_match_scan`.
    """
    if x < y:
        return x
    return y

#### Divide and conquer solution

def parens_match_dc(mylist):
    """
    Calls parens_match_dc_helper. If the result is (0,0),
    that means there are no unmatched parentheses, so the input is valid.
    
    Returns:
      True if parens_match_dc_helper returns (0,0); otherwise False
    """
    # done.
    n_unmatched_left, n_unmatched_right = parens_match_dc_helper(mylist)
    return n_unmatched_left==0 and n_unmatched_right==0

def parens_match_dc_helper(mylist):
    # base cases
    if len(mylist) == 0:
        return (0, 0)

    if len(mylist) == 1:
        if mylist[0] == '(':
            return (0, 1)
        elif mylist[0] == ')':
            return (1, 0)
        else:
            return (0, 0)

    # recursive case
    mid = len(mylist) // 2

    left_R, left_L = parens_match_dc_helper(mylist[:mid])
    right_R, right_L = parens_match_dc_helper(mylist[mid:])

    # Match unmatched left parentheses from the left half
    # with unmatched right parentheses from the right half.
    matched = min(left_L, right_R)

    R = left_R + right_R - matched
    L = left_L + right_L - matched

    return (R, L)