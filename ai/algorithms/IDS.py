import time

from ai.algorithms.DLS import DLS


# Iterative deepening search, uses DLS ( Deep limited Search) for infinity times, until solution found or time limit
# exceeded.
class IDS:
    start_time = 0

    @staticmethod
    def start_ids(initial_state, time_limit):
        IDS.start_time = time.time()
        i = 1
        curr_time = time.time() - IDS.start_time
        while curr_time < time_limit:
            solution_state = DLS.start_dls(initial_state, i)
            if solution_state is None:
                i += 1
                curr_time = time.time() - IDS.start_time
                continue
            else:
                print("Problem solved in " + str(time.time() - IDS.start_time)+" seconds.")
                print("Solution: " + solution_state.get_solution_path() + solution_state.get_last_move())
                curr_time = time.time() - IDS.start_time
                break
        if curr_time > time_limit:
            print("IDS Failed to solve the problem in " + str(time_limit) + " seconds")
        DLS.reset_stack()
        IDS.start_time = 0
