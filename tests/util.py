import numpy as np


def generate_sound(frequency, duration_second, sample_rate):
    ## 1 sec length time series with sampling rate
    ts1sec = list(np.linspace(0, np.pi * 2 * frequency, sample_rate))
    ## 1 sec length time series with sampling rate
    ts = ts1sec * duration_second
    return np.sin(ts)
