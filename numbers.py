import random
import sys

problems = 20

def maybe_add_spacer(s, what):
    if s != "":
        return s + what 
    return s

def gen_problem():
    r = random.randint(1000, 999999999)
    millions = int(r / 1000000)
    r = r - millions * 1000000
    thousands = int(r / 1000)
    r = r - thousands * 1000
    hundreds = int(r / 100);
    r = r - hundreds * 100;

    if random.randint(0, 3) == 0:
        millions = 0
    if random.randint(0, 3) == 0:
        thousands = 0
    if random.randint(0, 3) == 0:
        hundreds = 0
    if millions == 0 and thousands == 0 and hundreds == 0:
        hundreds = random.randint(1,99)

    s = ""
    if millions > 0:
        hundred_million = int(millions / 100)
        millions = millions - hundred_million * 100
        if hundred_million > 0:
            s = str(hundred_million) + " hundred"
        if millions > 0:
            s = maybe_add_spacer(s, " and ") + str(millions)
        s = s + " million"
    if thousands > 0:
        hundred_thousand = int(thousands / 100)
        thousands = thousands - hundred_thousand * 100
        if hundred_thousand > 0:
            s = maybe_add_spacer(s, " ") + str(hundred_thousand) + " hundred"
        if thousands > 0:
            s = maybe_add_spacer(s, " and ") + str(thousands)
        s = s + " thousand"
    if hundreds > 0:
        s = maybe_add_spacer(s, " ") + str(hundreds) + " hundred"
    if r > 0:
        s = maybe_add_spacer(s, " and ")  + str(r)
    print(s)

for i in range(0, problems):
    gen_problem()
    print("")






