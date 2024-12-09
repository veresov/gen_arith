#Configuration
con_limit = 100                               # Limit on constants (how big individual constant terms can get)
result_limit = 999                            # Limit on the result value
mul_result_limit = 600                        # Limit on a result of any multiplication
div_denominator_limit = 100                   # Limit on the denominator
terms = 4                                     # How many terms are in the expression (upper limit)
allow_add = True                              # +
allow_sub = True                              # -
allow_mul = True                              # *
allow_div = True                              # /
allow_paren = True                            # ()
wrap_num = True                               # Put parenthesis around numerator to disambiguate left associativity
print_answers = False                         # Prints answers after excercises
print_line_numbers = True                     # Useful if printing answers
equation = False                              # Generate equations instead of number sentenses
spacing = 2                                   # Number of empty lines in between
expression = False                            # Simplify expression mode


import random
import math
import sys

ADD = 0
SUB = 1
MUL = 2
DIV = 3
PAREN = 4
CON = 5
VAR = 6
DEAD = 666

equation_variable = (DEAD, "", 0, True)

def random_boolean():
    return random.choice([0,1]) == 1

def set_equation_variable(node):
    global equation_variable
    equation_variable = node

def has_equation_variable():
    (op, _, _, _) = equation_variable
    if op == DEAD:
        return False
    return True

def prio(op):
    if op == CON or op == VAR:
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
        if equation and not has_equation_variable():
            x = var(min(value_limit, con_limit), "x")
            set_equation_variable(x)
            return x
        elif expression and random_boolean():
            return var(min(value_limit, con_limit), random.choice(["x","y","z"]))
        else:
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
    return (CON, 1, "1", False);

def con(value_limit):
    v = random.randint(0, min(value_limit, con_limit))
    return (CON, v, str(v), False)

def var(value_limit, name):
    (_, value, _, _) = con(value_limit)
    return (VAR, value, name, True)

def add(term_limit, value_limit):
    n = int(term_limit / 2)
    v = int(random.randint(0, value_limit))
    l = root(n, v, False)
    r = root(term_limit - n, value_limit - v, False)
    if random_boolean():
        t = l
        l = r
        r = t
    (_, lvalue, ltext, lvar) = wrap_low_prio_left(l, ADD)
    (_, rvalue, rtext, rvar) = wrap_low_prio_right(r, ADD)
    return (ADD, lvalue + rvalue, ltext + " + " + rtext, lvar or rvar)

def sub(term_limit, value_limit):
    n = int(term_limit / 2)
    l = int(random.randint(0, value_limit))
    (_, lvalue, ltext, lvar) = wrap_low_prio_left(root(n, l, False), SUB)
    l = value_limit - l
    (_, rvalue, rtext, rvar) = wrap_negative_con(wrap_low_prio_right(root(term_limit - n, l, False), SUB))
    return (SUB, lvalue - rvalue, ltext + " - " + rtext, lvar or rvar)

def mul(term_limit, value_limit):
    n = int(term_limit / 2)
    v = int(random.randint(0, int(math.sqrt(value_limit))))
    l = root(n, v, False)
    (lop, lvalue, ltext, lvar) = l
    if lvalue == 0 and value_limit > 0 and lvar == False:
        l = con(value_limit)
        if lvalue == 0:
            l = one()

    if lvalue != 0:
        v = int(value_limit / abs(lvalue))
    r = root(term_limit - n, v, False)
    (rop, rvalue, rtext, rvar) = r
    if rvalue == 0 and value_limit > 0 and rvar == False:
        r = con(v)
        if rvalue == 0:
            r = one()

    if random_boolean():
        t = l
        l = r
        r = t

    (lop, lvalue, ltext, lvar) = wrap_low_prio_left(l, MUL)
    (rop, rvalue, rtext, rvar) = wrap_low_prio_right(r, MUL)

    return (MUL, lvalue * rvalue, ltext + " * " + rtext, lvar or rvar)

def div(term_limit, value_limit):
    n = int(term_limit / 2)
    l = root(n, value_limit, False)
    r = root(term_limit - n, min(div_denominator_limit, value_limit), False)

    # Make sure the result is > 1. Swap left and right if necessary
    if l[1] < r[1]:
        t = r
        r = l
        l = t

    (lop, lvalue, ltext, lvar) = wrap_low_prio_left(l, DIV)
    (rop, rvalue, rtext, rvar) = wrap_low_prio_right(r, DIV)

    # Avoid divisions by zero,
    if rvalue == 0:
        if rvar != True:
            # replace the right part with 1
            rvalue = 1
            rtext = "1"
        else:
            return (lop, lvalue, ltext, lvar)

    # Subtract the remainder from the left part so that it divides evenly
    remainder = int(lvalue % rvalue)
    if remainder != 0:
        lvalue = lvalue - remainder
        sign = " - " if remainder > 0 else " + "
        ltext = "(" + ltext + sign + str(abs(remainder)) + ")"

    return (DIV, int(lvalue / rvalue), ltext + " / " + rtext, lvar or rvar)

def paren(term_limit, value_limit):
    v = root(term_limit, value_limit, True)
    return (PAREN, v[1], "(" + v[2]  + ")", v[3])

def wrap_negative_con(t):
    (op, value, text, var) = t
    if op == CON and value < 0:
        return (PAREN, value, "(" + text + ")", var)
    return t

def wrap_low_prio_left(t, this_op):
    (op, value, text, var) = t
    if op == CON or op == VAR:
        return t;
    if prio(this_op) > prio(op):
        return (PAREN, value, "(" + text + ")", var)
    if wrap_num and this_op == DIV and op != PAREN:
        return (PAREN, value, "(" + text + ")", var)
    return t

def wrap_low_prio_right(t, this_op):
    (op, value, text, var) = t
    if op == CON or op == VAR:
        return t;
    if prio(this_op) > prio(op) or (prio(this_op) == prio(op) and (not is_associative(this_op) or not is_associative(op))):
        return (PAREN, value, "(" + text + ")", var)
    return t

def line_number_str(i):
    return str(i) + ":\t" if print_line_numbers else ""

results = []
num_lines = 25 if len(sys.argv) <= 1 else int(sys.argv[1])

for i in range(1, num_lines + 1):
    (_, value, text, _) = root(terms, result_limit, True)
    print(line_number_str(i) + text + " = " + (str(value) if equation else ""))
    if equation:
        (_, x, _, _) = equation_variable
        results.append(x)
        set_equation_variable((DEAD, 0, "", True))
    else:
        results.append(value)
    for l in range(0, spacing - 1):
        print("")

if print_answers:
    print("---------------")
    for i in range(1, num_lines + 1):
        print(line_number_str(i) + str(results[i - 1]))


