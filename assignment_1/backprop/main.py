'''
DO NOT CHANGE THIS SCRIPT
'''

from ast import literal_eval
import argparse, csv

import parsing, building, executing
ROUND = 2 ## we round results to two decimal places for checking


def load_math_problems():
    '''
    loading math problems from tsv file
    RETURN: math_problems as list of dicts
    ## (1) problem: math equation as string
    ## (2) input_vars: dict of corresponding input variables
    ## (3) output: output solution of the math problem
    ## (4) derivative: dict of the input variables derivatives
    '''

    ## load math problems
    parser = argparse.ArgumentParser()
    parser.add_argument("--problems", "-problems", help="absolute path to math problems", type=str, default="problems.tsv")
    args = parser.parse_args()

    math_problems = []
    with open(args.problems, "r") as fd:
        rd = csv.DictReader(fd, delimiter="\t")
        for row in rd:
            math_problems.append({str(k): literal_eval(v) for k, v in row.items()})
    return math_problems



def test_backprop(math_problems):

    ## set up parser
    p = parsing.Parser()

    ## iterate through math problems
    for i, math_problem in enumerate(math_problems):

        ## Step 1 ________________
        ## the math problem is parsed into infix notation
        infix_str, in_vars = p.parse(math_problem["problem"], in_vars = math_problem["in_vars"])
        ## Step 2 ________________
        ## take infix_str and in_vars and build a computation graph
        ## it is not required that parallel executions are parallelized
        b = building.Builder(infix = infix_str, in_vars = in_vars)

        ## Step 3 ________________
        ## execute the edges
        ## your method should set float output: x and dict derivative: {'y': -1.0, 'x': 1.0}
        e = executing.Executor(graph = b.graph, in_vars=in_vars)
        e.forward()
        e.backward()

        ## Step 4 ________________
        ## we are testing our solution
        ## output --> float comparison
        print(f"\n{str(i)}: problem: {math_problem['problem']}, in_vars: {math_problem['in_vars']}")
        if round(e.output,2) == round(math_problem["output"], ROUND):
            print(f"SUCCESS output: {round(e.output, ROUND)}")
        else:
            print(f"FAILURE output: {round(e.output, ROUND)} != {math_problem['output']}")

        ## first derivative --> dict comparison
        true_deriv = {k: round(v, ROUND) for k, v in math_problem["derivative"].items()}
        e.derivative = {k: round(v,ROUND) for k,v in e.derivative.items()}
        if e.derivative == true_deriv:
            print(f"SUCCESS derivative: {e.derivative}")
        else:
            print(f"FAILURE derivative: {e.derivative} != {math_problem['derivative']}")


if __name__ == '__main__':

    math_problems = load_math_problems()
    test_backprop(math_problems)





