
# =========================================
#  Created by: Kenny Davila Castellanos
#      For: CSC 480 - AI 1
#
#  TODO: Modified by: ???
#  TODO: Modified When: ???
# =========================================

from .operand import Operand
from .operator import Operator
class OperatorTree:
    def __init__(self, root):
        # this is a "private" attribute of the class
        self.__root = root

    def evaluate(self):
        # DONE: evaluate the expression .. starting from the roo
        return self.__root.evaluate()

    def post_order_list(self):
        # DONE: create a post-order traversal .. starting from the root
        # HINT: you will need a list to put the results.
        result = []
        self.__root.post_order_list(result)
        return result

    @staticmethod
    def build(json_data):
        is_leaf = bool(json_data["type"] == "number")
        if is_leaf:
            return Operand.BuildFromJSON(json_data["value"])
        else:
            # recursive call to create children
            left_node = OperatorTree.build(json_data["operands"][0])
            right_node = OperatorTree.build(json_data["operands"][1])
            children = [left_node, right_node]
            # create operator node
            operation_node = Operator.BuildFromJSON(json_data["value"], children)
            return operation_node

    # DONE: This function should create the tree using the provided JSON data
    #       this might need to check the type of the root node because
    #       root could be either an Operator or an Operand
    #
    # DONE: after creating the tree, it should return an instance of this
    #       class (OperatorTree), with the root value properly set up as the
    #       root node of the tree.
    @staticmethod
    def BuildFromJSON(json_data):
        root = OperatorTree.build(json_data["operator_tree"])
        return OperatorTree(root)


