import time
from datetime import datetime, timedelta

import numpy as np
from promise import Promise


def generate_sound(frequency, duration_second, sample_rate):
    ## 1 sec length time series with sampling rate
    ts1sec = list(np.linspace(0, np.pi * 2 * frequency, sample_rate))
    ## 1 sec length time series with sampling rate
    ts = ts1sec * duration_second
    return np.sin(ts)


# noinspection PyBroadException
def try_until(predicate, delay_between_try_ms, max_delay_ms) -> Promise:
    begin_time = datetime.now()
    end_time = begin_time + timedelta(milliseconds=max_delay_ms)

    while True:
        try:
            b = predicate()
            if b:
                print(f'predicate OK after {datetime.now() - begin_time}')
                return Promise.resolve(True)
        except Exception as ex:
            if datetime.now() >= end_time:
                return Promise.reject(ex)
            time.sleep(delay_between_try_ms / 1000)
        # too much time, but no exception
        if datetime.now() >= end_time:
            return Promise.reject(TimeoutError())
