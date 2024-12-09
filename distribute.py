import random
import sys

problems = 100

def gen_con():
    return str(random.randint(1, 20))
def gen_var():
    return random.choice(["x","y","z"]);

def gen_var_or_con():
    if random.choice([0, 1]) == 1:
        return gen_con()
    else:
        return gen_var()


def gen_paren():
    l = gen_var()
    l_is_var = True
    if random.choice([0, 1]) == 1:
        l = gen_con()
        l_is_var = False
    if l_is_var:
        r = gen_var_or_con()
    else:
        r = gen_var()

    return "(" + l + random.choice([" + ", " - "]) + r + ")"


def gen_x():
    if random.choice([0, 1]) == 1:
        return gen_var_or_con()
    else:
        return gen_paren()

def gen():
    return gen_paren() + gen_paren()


for i in range(0, problems):
    print(gen() + " = ")
    print("")






