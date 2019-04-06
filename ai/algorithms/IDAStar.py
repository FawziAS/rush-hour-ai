import time

from ai.algorithms.AStar import AStar
from ai.utils.Difficulty import Difficulty


class IDAStar:
    searched_nodes = 0
    num_of_nodes = 0
    start_time = 0
    finishing_time = 0

    @staticmethod
    def start_idas(initial_state_representation, heuristic, time_limit):
        IDAStar.reset()
        IDAStar.start_time = time.time()
        i = 0
        curr_time = time.time() - IDAStar.start_time
        while curr_time < time_limit:
            success = AStar.start_a_star(initial_state_representation, heuristic, time_limit, Difficulty.NOT_DEFINED, i)
            IDAStar.searched_nodes += AStar.searched_nodes
            IDAStar.num_of_nodes += AStar.nodes_num
            if success:
                IDAStar.finishing_time = time.time()
                print(IDAStar.get_game_info())
                # print("-----last iteration result-----")
                # print(AStar.get_game_info())
                break
            else:
                i += 1
                curr_time = time.time() - IDAStar.start_time

    @staticmethod
    def reset():
        IDAStar.searched_nodes = 0
        IDAStar.num_of_nodes = 0

    @staticmethod
    def get_game_info():
        info = ""
        info += "IDAStar Solved in: " + str(IDAStar.finishing_time - IDAStar.start_time) + " Seconds.\n"
        info += "IDAStar SearchedNodes: " + str(IDAStar.searched_nodes) + "\n"
        info += "IDAStar EBF: " + str(IDAStar.num_of_nodes / IDAStar.searched_nodes) + "\n"
        return info
