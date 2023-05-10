from function.classes import F, Step


def get_f(steps: list[Step]):
    f = F([], [])
    f.set_steps(steps)

    return f


def get_all_intervals(f: F)-> list[F]:
    # get all the possible intervals
    intervals = []
    for i in range(len(f.steps)):
        for j in range(len(f.steps)):
            ss = f.get_sub_steps(i, j)
            if modal_steps(ss):
                intervals.append(ss)
    return [get_f(i) for i in intervals]


def modal_steps(steps: list[Step])-> bool:
    if len(steps) <= 2:
        return True
    is_increasing = steps[0].get_gain() < steps[1].get_gain()
    for i in range(len(steps)-1):
        next_increase = steps[i].get_gain() < steps[i+1].get_gain()
        if is_increasing != next_increase:
            return True
    return False
