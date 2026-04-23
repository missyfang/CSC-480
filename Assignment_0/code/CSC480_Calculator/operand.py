
# =========================================
#  Created by: Kenny Davila Castellanos
#      For: CSC 480 - AI 1
#
# DONE: Modified by: Mellissa Fang
# DONE: Modified When: 04/08/26
# =========================================

# I.E NUMBER

from .operator_tree_element import OperatorTreeElement


class Operand(OperatorTreeElement):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self):
        # Overrides the evaluate function from parent class.
        # DONE: return it's current value
        return self._value

    def post_order_list(self, out_list):
        # Overrides the post_order_list function from parent class.
        # DONE: Should just add itself to the stack
        out_list.append(self)

    @staticmethod
    def BuildFromJSON(json_data):

        # Overrides the BuildFromJSON function from parent class.
        # DONE: Use JSON data to create a valid Operand Object
        #       this function assumes that json_data only contains the info for an Operand Node
        return Operand(json_data)

