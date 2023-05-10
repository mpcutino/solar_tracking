from function.classes import F
from solver.utils import get_all_intervals, get_f
from solver.dp import discrete_optimal, steps_from_d_table
from solver.gl import max_irradiance_steps


def general_solution(f: F, m: int):
    td = discrete_optimal(f, m-1)
    # print(td)
    all_intervals = get_all_intervals(f)
    omega = len(f)

    max_gain, max_intervals = -1, []
    # combine the solution from D and G
    for l in range(omega):
        ## get the optimal value for length l
        intervals_idx = steps_from_d_table(all_intervals, td, m-1, l)
        # print(intervals_idx)
        selected_intervals = [all_intervals[i] for i in intervals_idx]
        ## get the used length
        slens = sum([len(i) for i in selected_intervals])

        target_len = omega - slens
        final_interval = get_f(max_irradiance_steps(f, target_len))

        discrete_gain = sum([i.get_irradiance() for i in selected_intervals])
        semi_discrete_gain = final_interval.get_irradiance()
        if max_gain < discrete_gain + semi_discrete_gain:
            max_gain = discrete_gain + semi_discrete_gain
            max_intervals = selected_intervals + [final_interval]

    return max_gain, max_intervals
