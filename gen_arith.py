#Configuration
con_limit = 25                                # Limit on constants (how big individual constant terms can get)
result_limit = 300                            # Limit on the result value
mul_result_limit = 100                        # Limit on a result of any multiplication
div_denominator_limit = 6                     # Limit on the denominator
terms = 5                                     # How many terms are in the expression (upper limit)
allow_add = True                              # +
allow_sub = True                              # -
allow_mul = True                              # *
allow_div = True                              # /
allow_paren = True                            # ()
wrap_num = True                               # Put parenthesis around numerator to disambiguate left associativity
print_answers = False                         # Prints answers after excercises
print_line_numbers = False                    # Useful if printing answers


import random
import math
import sys

ADD = 0
SUB = 1
MUL = 2
DIV = 3
PAREN = 4
CON = 5

def prio(op):
    if op == CON:
        return 0;
    if op == ADD or op == SUB:
        return 1;
    if op == MUL or op == DIV:
        return 2;
    if op == PAREN:
        return 99;

def is_associative(op):
    if op == ADD or op == MUL:
        return True;
    if op == SUB or op == DIV:
        return False;
    return False


def root(term_limit, value_limit, not_paren):
    if term_limit <= 1:
        return con(min(value_limit, con_limit))
    else:
        ops = []
        if allow_add:
            ops.append(ADD)
        if allow_sub:
            ops.append(SUB)
        if allow_mul:
            ops.append(MUL)
        if allow_div:
            ops.append(DIV)
        if not not_paren and allow_paren:
            ops.append(PAREN)

        op = random.choice(ops)
        if op == ADD:
            return add(term_limit, value_limit)
        elif op == SUB:
            return sub(term_limit, value_limit)
        elif op == MUL:
            return mul(term_limit, min(value_limit, mul_result_limit))
        elif op == DIV:
            return div(term_limit, value_limit)
        elif op == PAREN:
            return paren(term_limit, value_limit)
    return ""

def one():
    return (CON, 1, "1");

def con(value_limit):
    v = random.randint(0, min(value_limit, con_limit))
    return (CON, v, str(v))

def add(term_limit, value_limit):
    n = int(term_limit / 2)
    l = int(random.randint(0, value_limit))
    (_, lvalue, ltext) = wrap_low_prio_left(root(n, l, False), ADD)
    l = value_limit - l
    (_, rvalue, rtext) = wrap_low_prio_right(root(term_limit - n, l, False), ADD)
    return (ADD, lvalue + rvalue, ltext + " + " + rtext)

def sub(term_limit, value_limit):
    n = int(term_limit / 2)
    l = int(random.randint(0, value_limit))
    (_, lvalue, ltext) = wrap_low_prio_left(root(n, l, False), SUB)
    l = value_limit - l
    (_, rvalue, rtext) = wrap_negative_con(wrap_low_prio_right(root(term_limit - n, l, False), SUB))
    return (SUB, lvalue - rvalue, ltext + " - " + rtext)

def mul(term_limit, value_limit):
    n = int(term_limit / 2)
    l = int(random.randint(0, int(math.sqrt(value_limit))))
    (_, lvalue, ltext) = wrap_low_prio_left(root(n, l, False), MUL)
    if lvalue == 0 and value_limit > 0:
        (_, lvalue, ltext) = con(value_limit)
        if lvalue == 0:
            (_, lvalue, ltext) = one()
    if lvalue != 0:
        l = int(value_limit / abs(lvalue))
    (_, rvalue, rtext) = wrap_low_prio_right(root(term_limit - n, l, False), MUL)
    if rvalue == 0 and value_limit > 0:
        (_, rvalue, rtext) = con(l)
        if rvalue == 0:
            (_, rvalue, rtext) = one()
    return (MUL, lvalue * rvalue, ltext + " * " + rtext)

def div(term_limit, value_limit):
    n = int(term_limit / 2)
    l = root(n, value_limit, False)
    r = root(term_limit - n, min(div_denominator_limit, value_limit), False)

    # Make sure the result is > 1. Swap left and right if necessary
    if l[1] < r[1]:
        t = r
        r = l
        l = t

    (_, lvalue, ltext) = wrap_low_prio_left(l, DIV)
    (_, rvalue, rtext) = wrap_low_prio_right(r, DIV)

    # Avoid divisions by zero, replace the right part with 1
    if rvalue == 0:
        rvalue = 1
        rtext = "1"

    # Subtract the remainder from the left part so that it divides evenly
    remainder = int(lvalue % rvalue)
    if remainder != 0:
        lvalue = lvalue - remainder
        sign = " - " if remainder > 0 else " + "
        ltext = "(" + ltext + sign + str(abs(remainder)) + ")"

    return (DIV, int(lvalue / rvalue), ltext + " / " + rtext)

def paren(term_limit, value_limit):
    v = root(term_limit, value_limit, True)
    return (PAREN, v[1], "(" + v[2]  + ")")

def wrap_negative_con(t):
    (op, value, text) = t
    if op == CON and value < 0:
        return (PAREN, value, "(" + text + ")")
    return t

def wrap_low_prio_left(t, this_op):
    (op, value, text) = t
    if op == CON:
        return t;
    if prio(this_op) > prio(op):
        return (PAREN, value, "(" + text + ")")
    if wrap_num and this_op == DIV and op != PAREN:
        return (PAREN, value, "(" + text + ")")
    return t

def wrap_low_prio_right(t, this_op):
    (op, value, text) = t
    if op == CON:
        return t;
    if prio(this_op) > prio(op) or (prio(this_op) == prio(op) and (not is_associative(this_op) or not is_associative(op))):
        return (PAREN, value, "(" + text + ")")
    return t

def line_number_str(i):
    return str(i) + ":\t" if print_line_numbers else ""

results = []
num_lines = 25 if len(sys.argv) <= 1 else int(sys.argv[1])

for i in range(1, num_lines + 1):
    (_, value, text) = root(terms, result_limit, True)
    print(line_number_str(i) + text + " = ")
    results.append(value)

if print_answers:
    print("---------------")
    for i in range(1, num_lines + 1):
        print(line_number_str(i) + str(results[i - 1]))


