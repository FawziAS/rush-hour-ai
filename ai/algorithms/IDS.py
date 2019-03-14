from ai.algorithms.DLS import DLS


class IDS:

    @staticmethod
    def start_ids(initial_state):
        i = 1
        while i<10000:
            solution_state = DLS.start_dls(initial_state, i)
            if solution_state is None:
                i += 1
            else:
                print("Solution: " + solution_state.get_solution_path() + solution_state.get_last_move())
                break
        print("IDS Failed to solve")
        DLS.reset_stack()
