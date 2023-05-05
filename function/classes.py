import numpy as np
import matplotlib.pyplot as plt


class Interval:

    def __init__(self, low: int, up: int) -> None:
        assert low <= up, "bad interval definition"
        self.low = low
        self.up = up
    
    def get_up(self):
        return self.up
    
    def get_low(self):
        return self.low

    def copy(self):
        return type(self)(self.low, self.up)

    def __len__(self):
        return self.up - self.low
    
    def __str__(self) -> str:
        return "{0}, {1}".format(self.low, self.up)


class Step:

    def __init__(self, interval: Interval, alpha: float) -> None:
        self.interval = interval
        self.alpha = alpha
    
    def get_gain(self):
        return self.__get_gain__(self.interval)
    
    def crop_end(self, end):
        self.interval = Interval(self.interval.get_low(), end)
    
    def crop_start(self, start):
        self.interval = Interval(start, self.interval.get_up())
    
    def get_left_gain(self, theta):
        ni = Interval(self.interval.get_low(), theta)
        return self.__get_gain__(ni)
    
    def get_right_gain(self, theta):
        ni = Interval(theta, self.interval.get_up())
        return self.__get_gain__(ni)
    
    def get_xy_plot(self):
        xs = [self.interval.get_low(), self.interval.get_up()]
        ys = [self.alpha, self.alpha]
        return xs, ys
    
    def copy(self):
        return type(self)(self.interval.copy(), self.alpha)

    def __get_gain__(self, interval: Interval)-> int:
        return len(interval)*self.alpha
    
    def __len__(self):
        return len(self.interval)
    
    def __str__(self):
        return "{0}, {1}".format(self.interval, self.alpha)


class F:

    def __init__(self, steps: list[int], alphas: list[int]) -> None:
        assert len(steps) == len(alphas), "length of steps does not match the length of alpha values"
        # get the steps
        nsteps = []
        for i in range(len(steps)-1):
            l, u = int(steps[i]), int(steps[i+1])
            a = alphas[i]
            interval = Interval(l, u)
            nsteps.append(Step(interval, a))
        self.set_steps(nsteps)

    def set_steps(self, steps: list[Step]):
        self.steps = steps
        self.omega = sum([len(s) for s in self.steps])
    
    def get_sub_steps(self, star_idx=0, end_idx=180):
        return self.steps[star_idx:end_idx+1]
    
    def get_irradiance(self):
        return sum([s.get_gain() for s in self.steps])
    
    def plot(self, axis=None, **plot_kwargs):
        xs, ys = zip(*[s.get_xy_plot() for s in self.steps])

        if axis is None:
            plt.plot(np.ravel(xs), np.ravel(ys), **plot_kwargs)
            plt.show()
            plt.close()
        else:
            axis.plot(np.ravel(xs), np.ravel(ys), **plot_kwargs)
    
    def __len__(self):
        return self.omega
