# gen_arith.py
Arithmetic exercise generator for kids

At the beginning of the file there is the following configuration. Adjust as needed.

    con_limit = 99                                # Limit on constants (how big individual constant terms can get)
    result_limit = 100                            # Limit on the result value
    mul_result_limit = 100                        # Limit on a result of any multiplication
    terms = 3                                     # How many terms are in the expression
    allow_add = True                              # +
    allow_sub = False                             # -
    allow_mul = False                             # *
    allow_div = False                             # /
    allow_paren = False                           # ()
    print_answers = False                         # Prints answers after excercises
    print_line_numbers = False                    # Useful if printing answers

# word_problems.py
Generate simple word problems, where the statements are chained with addition, subtraction and multiplication.

    Kate has 4 lions.
    Maddie has 5 times more turtles than Kate has lions. 
    Lucy has 14 less cats than Maddie has turtles.
    Charlie has 5 times more cows than Lucy has cats.
    How many cows does Charlie have?
