import numpy as np

from function.classes import F
from solver.utils import get_all_intervals


def discrete_optimal(f: F, m: int) -> np.array:
    omega = len(f)
    
    return __D__(get_all_intervals(f), m, omega)


def __D__(intervals: list[F], m: int, target_len: int) ->  np.array:
    # we add one because of the 0-based indexing
    m += 1
    target_len += 1
    nsteps = len(intervals) + 1
    table_D = np.zeros((nsteps, m, target_len))

    for i in range(nsteps):
        zero_based_i = i - 1
        for j in range(m):
            for l in range(target_len):
                i_len = len(intervals[zero_based_i])
                if 0 in [i, j, l]:
                    table_D[i, j, l] = 0
                elif l < i_len:
                    table_D[i, j, l] = table_D[i-1, j, l]
                else:
                    current_gain = intervals[zero_based_i].get_irradiance() + table_D[i, j-1, l-i_len]
                    table_D[i, j, l] = max(table_D[i-1, j, l], current_gain)
    return table_D


def steps_from_d_table(intervals: list[F], table: np.array, m: int, l: int) -> list[int]:
    assert len(intervals) + 1 == table.shape[0], "intervals are assumed 0-based, while table 1-based indexing"
    selected_indexes = []

    current_i, current_j, current_l = table.shape[0] - 1, m, l
    while 0 not in [current_i, current_j, current_l]:
        current_value = table[current_i, current_j, current_l]
        if current_value == 0:
            selected_indexes.append(0)
            break
        if current_value == table[current_i - 1, current_j, current_l]:
            # the current index was not selected
            current_i -= 1
            continue
        # the current index was selected
        selected_indexes.append(current_i)
        # update j and l
        current_j -= 1
        current_l -= len(intervals[current_i-1])
    # normalize to 0-based indexing
    return [i-1 for i in selected_indexes]
