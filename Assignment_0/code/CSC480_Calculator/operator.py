from unittest import case

# =========================================
#  Created by: Kenny Davila Castellanos
#      For: CSC 480 - AI 1
#
#  DONE: Modified by: Mellissa Fang
#  DONE: Modified When: 04/08/26
# =========================================


from .operator_tree_element import OperatorTreeElement
from .operand import Operand

class Operator(OperatorTreeElement):
    def __init__(self, value, children):
        super().__init__(value)
        # this is a "private" attribute of the class
        self.__children = children

    def evaluate(self):
        # Overrides the evaluate function from parent class.
        # DONE: apply the local operator and return the value
        #       - self._value == "+" ?
        #       - self._value == "*" ?
        #       - self._value == "-" ?
        #       - self._value == "/" ?
        left_child = self.__children[0].evaluate()
        right_child = self.__children[1].evaluate()
        match self._value:
            case "+":
                return left_child + right_child
            case "-":
                return left_child - right_child
            case "*":
                return left_child * right_child
            case "/":
                return left_child / right_child




        raise NotImplementedError()

    def post_order_list(self, out_list):
        # Overrides the post_order_list function from parent class.
        # DONE: Should add itself and its children ... all in post-order
        # hint: recursion is needed
        #left child
        self.__children[0].post_order_list(out_list)
        #right child
        self.__children[1].post_order_list(out_list)
        out_list.append(self)
        return out_list

    @staticmethod
    def BuildFromJSON(value, children):
        # Overrides the BuildFromJSON function from parent class.
        # DONE: Use  JSON data is used to create and return a valid Operator object
        #       which in turn requires recursively creating its children.
        #
        #  This function assumes that json_data contains the info for an Operator Node
        #     and all of its children, and children of its children, etc.


        return Operator(value, children)

