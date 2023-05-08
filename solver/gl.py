import numpy as np

from function.classes import F
from solver.utils import get_f


def max_irradiance_steps(f: F, target_len: int):
    """
    Compute G_l for the target length.
    It return the set of steps for which the max value is obtained. If one of the
    steps is not used in its full extension, it is cropped.
    """
                # right sweep
    # compute the ending interval for the index starting at the current position
    index2go = get_index2go(f, target_len, from_l2r=True)
    print(index2go)
    l2r_max_irr, l2r_max_steps = sweep_intervals(f, index2go, from_l2r=True)
    print(l2r_max_irr)

                # left sweep
    # compute the starting interval for the index ending at the current position
    index2go = get_index2go(f, target_len, from_l2r=False)
    print(index2go)
    r2l_max_irr, r2l_max_steps = sweep_intervals(f, index2go, from_l2r=False)
    print(r2l_max_irr)

    # get the maximum
    max_steps = l2r_max_steps if (l2r_max_irr >= r2l_max_irr) else r2l_max_steps
    # max_steps = l2r_max_steps
    return max_steps


def get_index2go(f, target_len, from_l2r: bool = True):
    """
    For a given position, get the index to go.
    At index i, the value of j indicates that: f from i to j is the portion of f such that
        f from i to j-1 is lower than target len, and f from i to j is bigger.
    When sweeping from left to right, i <= j, and in other case i >= j.
    """
    s_lens = np.cumsum([len(s) for s in f.steps])

    index2go = []
    added_value = 1 if from_l2r else -1
    current_end = 0 if from_l2r else (len(f.steps) - 1)
    iterate_steps = f.steps if from_l2r else reversed(f.steps)
    for i, s in enumerate(iterate_steps):
        if not from_l2r:
            i = len(f.steps) - 1 - i
        while (0 <= current_end < len(f.steps)):
            if from_l2r:
                current_len = s_lens[current_end] - s_lens[i] + len(s)
            else:
                current_len = s_lens[i] - s_lens[current_end] + len(s)
            sweep_stop_cnd = (current_end >= i) if from_l2r else (current_end <= i)
            if current_len >= target_len and sweep_stop_cnd:
                break
            current_end += added_value
        # get a feasible end value
        if from_l2r:
            current_end = min(current_end, len(f.steps) - 1)
        else:
            current_end = max(current_end, 0)
        index2go.append(current_end)
    
    if from_l2r:
        return index2go
    return list(reversed(index2go))


def sweep_intervals(f, index2go, from_l2r: bool=True):
    cum_sum = np.cumsum([len(s) for s in f.steps])

    max_irradiance, max_steps = -1, []
    
    for i, j in enumerate(index2go):
        min_idx, max_idx = min(i, j), max(i, j)

        sub_steps = f.get_sub_steps(min_idx, max_idx)

        # crop the last step, if needed
        if from_l2r:
            len_prev = (cum_sum[j-1] - cum_sum[i] + len(f.steps[i])) if j > 0 else 0
        else:
            len_prev = (cum_sum[i] - cum_sum[j+1] + len(f.steps[j+1]) if j < len(f.steps) - 1 else 0)
        len_current = cum_sum[max_idx] - cum_sum[min_idx] + len(f.steps[min_idx])
        crop_len = len_current - len_prev

        jstep = f.steps[j].copy()
        if from_l2r:
            jstep.crop_end(jstep.interval.get_low() + crop_len)
            sub_steps[-1] = jstep
        else:
            jstep.crop_start(jstep.interval.get_up() - crop_len)
            sub_steps[0] = jstep
        # get the irradiance
        new_f = get_f(sub_steps)
        if max_irradiance < new_f.get_irradiance():
            max_irradiance = new_f.get_irradiance()
            max_steps = new_f.steps
            # print(i, j)

    return max_irradiance, max_steps
