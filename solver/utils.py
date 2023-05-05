from function.classes import F, Step


def get_f(steps: list[Step]):
    f = F([], [])
    f.set_steps(steps)

    return f
