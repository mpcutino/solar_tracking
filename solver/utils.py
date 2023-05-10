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
            intervals.append(f.get_sub_steps(i, j))
    return [get_f(i) for i in intervals]
