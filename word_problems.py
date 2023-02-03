import random
import sys

problems = 5
sentences = 4

def object_str(o, c):
    if c > 1:
        return o + "s"
    return o

def gen_problem():
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Francis", "George", "Hanna", "Igor", "Jessica", "Kate", "Lucy", "Maddie", "Nancy", "Olga", "Peter" ]
    objects = [ "cat", "dog", "turtle", "pig", "cow", "horse", "lion", "tiger", "elephant"]

    MORE = 0
    LESS = 1
    TIMES_MORE = 2
    ops = 3

    need_relation = False
    prev_name = ""
    prev_object = ""
    cur_count = 0
    for i in range(0, sentences):
        n = random.choice(names)
        names.remove(n)
        o = random.choice(objects)
        objects.remove(o)
        c = random.randint(1,20)
        if need_relation:
            op = random.randint(0, ops - 1)
            r = ""
            if op == MORE:
                r = "more"
                cur_count = cur_count + c
            elif op == LESS:
                if cur_count < c:
                    r = "more"
                    cur_count = cur_count + c
                else:
                    r = "less"
                    cur_count = cur_count - c
            elif op == TIMES_MORE:
                c = random.randint(2,5)
                r = "times more"
                cur_count = cur_count * c
            print(n + " has " + str(c) + " " + r + " " + object_str(o, c) + " than " + prev_name + " has " + prev_object + "s.")
        else:
            print(n + " has " + str(c) + " " + object_str(o, c) + ".")
            need_relation = True
            cur_count = c

        prev_name = n
        prev_object = o

    print("How many " + prev_object + "s does " + prev_name + " have?")


for i in range(0, problems):
    gen_problem()
    print("")
