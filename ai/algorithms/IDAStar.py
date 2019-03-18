import time

from ai.algorithms.AStar import AStar


class IDAStar:
    @staticmethod
    def start_idas(initial_state_representation, heuristic, time_limit):
        IDAStar.start_time = time.time()
        i = 0
        while time.time() - IDAStar.start_time < time_limit:
            success = AStar.start_a_star(initial_state_representation, heuristic, 100, i)
            if success:
                print("Solution found!!!!")
                break
            else:
                i += 1
                AStar.reset()

