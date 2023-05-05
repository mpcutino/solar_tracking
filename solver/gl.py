from function.classes import F


def max_irradiance_steps(f: F, target_len: int):
    """
    Compute G_l for the target length.
    It return the set of steps for which the max value is obtained. If one of the
    steps is not used in its full extension, it is cropped.
    """

