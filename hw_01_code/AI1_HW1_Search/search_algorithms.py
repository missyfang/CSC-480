
"""
# ===============================================
#  Created by: Kenny Davila Castellanos
#              for CSC 380/480
#
#  MODIFIED BY: [Your NAME]
# ===============================================
"""

import time
import heapq
from collections import deque
from xml.sax.handler import property_dom_node

from . import search_tree_node
from .search_result import SearchResults
from .search_tree_node import SearchTreeNode

from AI1_HW_Problem.problem import Problem
from AI1_HW_Problem.search_request import SearchRequest

class SearchAlgorithms:
    BreadthFirstSearch = 0
    UniformCostSearch = 1
    AStarSearch = 2

    """
        Implementation of the Breadth-first Search (BFS) algorithm. The only input
        required is the problem, which includes a reference to current CityMap and 
        current Search Request. The function needs to compute and store search 
        results and other statistics inside of a SearchResults object. 
    """
    @staticmethod
    def breadth_first_search(problem: Problem) -> SearchResults:
        nodes_reached = 0
        nodes_explored = 0

        queue = deque()
        start = SearchTreeNode(None, None, problem.get_initial_state(), 0)
        # not adding start to reached bc we need to return
        reached_nodes = set()
        reached_nodes.add(start.get_state().get_representation())
        queue.append(start)
        solution_node = start
        while queue:
          current_node = queue.popleft()
         # print(f"exploring --> {current_node.get_state().get_location()} | visited: {current_node.get_state().get_visited_targets()}")
          if problem.is_goal_state(current_node.get_state()):
              solution_node = current_node
              break
          # expand state
          nodes_explored += 1
          children = problem.generate_children(current_node.get_state())
          for child in children:
              child_loc = child.get_location()
              child_node = SearchTreeNode(current_node, child.get_location(), child, 0)
              child_rep =child.get_representation()
              # if child already added to queue it will be explored don't re-add
              if child_rep not in reached_nodes:
                  nodes_reached += 1
                  reached_nodes.add(child_rep)
                  queue.append(child_node)

        return SearchResults(solution_node.path_to_root(), solution_node.get_path_cost(), nodes_reached, nodes_explored)

    """
        Implementation of the Uniform Cost Search (UCS) algorithm. The only input
        required is the problem, which includes a reference to current CityMap and 
        current Search Request. The function needs to compute and store search 
        results and other statistics inside of a SearchResults object. 
    """
    @staticmethod
    def uniform_cost_search(problem: Problem) -> SearchResults:
        # TODO
        nodes_reached = 0
        nodes_explored = 0

        queue = deque()
        start = SearchTreeNode(None, None, problem.get_initial_state(), 0)
        # not adding start to reached bc we need to return
        reached_nodes = dict()
        reached_nodes[start.get_state().get_representation()] = 0
        queue.append(start)
        solution_node = start
        while queue:
            current_node = queue.popleft()
            # print(
            #    f"exploring --> {current_node.get_state().get_location()} | visited: {current_node.get_state().get_visited_targets()}")
            if problem.is_goal_state(current_node.get_state()):
                solution_node = current_node
                break
            # expand state
            nodes_explored += 1
            children = problem.generate_children(current_node.get_state())
            for child in children:
                child_loc = child.get_location()
                #cost moving parent ot child
                cost = problem.get_action_cost(current_node.get_state(), child_loc)
                child_node = SearchTreeNode(current_node, child.get_location(), child, cost)
                child_rep = child.get_representation()
                # cost check to readd children to be explored again
                # if cost is less re add
                if child_rep not in reached_nodes or cost < reached_nodes[child_rep]:
                    nodes_reached += 1
                    reached_nodes[child_rep] = cost
                    queue.append(child_node)

        return SearchResults(solution_node.path_to_root(), solution_node.get_path_cost(), nodes_reached, nodes_explored)


    """
        Implementation of the A* Search algorithm. The only input
        required is the problem, which includes a reference to current CityMap and 
        current Search Request. The function needs to compute and store search 
        results and other statistics inside of a SearchResults object. 
    """
    @staticmethod
    def A_start_search(problem: Problem) -> SearchResults:
        # TODO: Your CODE HERE
        # use a prioroty queue to order nodes/
        return SearchResults(None, None, 0, 0)

    """
        Auxiliary function for printing search results 
    """
    @staticmethod
    def print_solution_details(test_case: SearchRequest, search_results: SearchResults, search_time: float):
        if search_results.get_solution() is None:
            print(" --> No Solution was found!")
        else:
            # this part is just for formatting... with highlight for important nodes in the path
            tempo_list = []
            for value in [test_case.get_start_location()] + search_results.get_solution():
                if value == test_case.get_start_location():
                    tempo_list.append(f"[{value}]")
                elif value in test_case.get_targets():
                    tempo_list.append(f"({value})")
                else:
                    tempo_list.append(value)
            full_path = " -> ".join(tempo_list)
            print(f" --> Solution found: {full_path}")
            print(f" --> Solution Cost: {search_results.get_cost()}")
        print(f" --> Nodes Reached: {search_results.reached_nodes_count()}")
        print(f" --> Nodes Explored: {search_results.explored_nodes_count()}")
        print(f" --> Search Time (s): {search_time}")

    """
        Auxiliary Function for running the search algorithm specified, 
        and printing the results and statistics.
    """
    @staticmethod
    def search(problem: Problem, algorithm: int):
        # Note: This code might look awkward, but this is intentional
        # the idea is to NOT count the print operation as part of the search time
        if algorithm == SearchAlgorithms.BreadthFirstSearch:
            print("\n - Running Breadth-First Search")
        elif algorithm == SearchAlgorithms.UniformCostSearch:
            print("\n - Running Uniform Cost Search")
        elif algorithm == SearchAlgorithms.AStarSearch:
            print("\n - Running A Star Search")
        else:
            raise Exception(f"Invalid Search Algorithm: {algorithm}")

        start_time = time.time()
        if algorithm == SearchAlgorithms.BreadthFirstSearch:
            solution = SearchAlgorithms.breadth_first_search(problem)
        elif algorithm == SearchAlgorithms.UniformCostSearch:
            solution = SearchAlgorithms.uniform_cost_search(problem)
        else:
            # by default, assume it is the A* algorithm
            solution = SearchAlgorithms.A_start_search(problem)
        end_time = time.time()
        total_time = end_time - start_time

        SearchAlgorithms.print_solution_details(problem.get_current_case(), solution, total_time)

