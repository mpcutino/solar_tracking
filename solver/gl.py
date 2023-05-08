import numpy as np

from function.classes import F, Step
from solver.utils import get_f


def max_irradiance_steps(f: F, target_len: int):
    """
    Compute G_l for the target length.
    It return the set of steps for which the max value is obtained. If one of the
    steps is not used in its full extension, it is cropped.
    """
    s_lens = np.cumsum([len(s) for s in f.steps])

    max_irradiance, max_steps = -1, []
    
                # right sweep
    # compute the ending interval for the index starting at the current position
    index2go = []
    current_end = 0
    for i, s in enumerate(f.steps):
        while (current_end < len(f.steps)):
            current_len = s_lens[current_end] - s_lens[i] + len(s)
            if current_len >= target_len and current_end >= i:
                break
            current_end += 1
        # get a feasible end value
        current_end = min(current_end, len(f.steps) - 1)
        index2go.append(current_end)
    
    for i, j in enumerate(index2go):
        sub_steps = f.get_sub_steps(i, j)
        # crop the last step, if needed
        len_prev = (s_lens[j-1] - s_lens[i] + len(f.steps[i])) if j > 0 else 0
        len_current = s_lens[j] - s_lens[i] + len(f.steps[i])
        crop_len = len_current - len_prev

        jstep = f.steps[j].copy()
        jstep.crop_end(jstep.interval.get_low() + crop_len)
        sub_steps[-1] = jstep
        # get the irradiance
        new_f = get_f(sub_steps)
        if max_irradiance < new_f.get_irradiance():
            max_irradiance = new_f.get_irradiance()
            max_steps = new_f.steps

                # left sweep: TODO
    # compute the starting interval for the index ending at the current position

    return max_steps
