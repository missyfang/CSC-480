
# =========================================
#  Created by: Kenny Davila Castellanos
#      For: CSC 480 - AI 1
#
#  TODO: Modified by: Mellissa Fang
#  TODO: Modified When: 04/04/26
# =========================================


import sys
import json

from CSC480_Calculator import OperatorTree, Operator, Operand


def stack_based_evaluation(post_order):
    # TODO: this is a simple evaluation algorithm, using a stack
    #       it sequentially reads the mathematical expression in post-fix notation
    #        - every time it finds an operand (A)
    #             it will simply put (A) on the stack
    #        - every time it finds an operator (OP)
    #             it will take 2 items from stack, (B) and (A)
    #             it must compute result by applying operator
    #                (RES) = (A) (OP) (B)
    #             it will save (RES) to the stack
    #             mind that the ORDER OF THE OPERANDS might affect the result
    #       it does it until the end.

    # Remember:
    #    If the expression is valid, only one item will be there at the end
    #    this is the solution, and must be returned
    #
    # HINT: use isinstance function to check the types of the elements on
    #       the post_order list

    # TODO: your logic here
    return 0.0


def main():
    # handling the command line arguments , given do not change!
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"\tpython {sys.argv[0]} filename")
        return

    # Step 1
    # DONE: Load the JSON data
    #     The actual filename to load should be on sys.argv ...
    #     * position 0 is always the path to the script
    #     * position 1 ... n are your custom command line arguments

    # DONE: Load the input File using the JSON library
    with open(sys.argv[1], 'r') as file:
        data = json.load(file)

    # Step 2
    # DONE: Load the expression from file using the OperatorTree.BuildFromJSON function
    # DONE: You must implement the functions
    #       - OperatorTree.BuildFromJSON
    #       - Operand.BuildFromJSON
    #       - Operator.BuildFromJSON
    tree = OperatorTree.BuildFromJSON(data)
    print(tree)

    # Step 3
    # TODO: Evaluate the expression (using the evaluate function of the OperatorTree class)

    # Step 4
    # TODO: Generate a list of the elements on the Operator Tree in post-order and print it!

    # Step 5
    # TODO: Evaluate the expression (again) but using the post fix notation and a stack
    #       This must be done by calling stack_based_evaluation



if __name__ == "__main__":
    main()

