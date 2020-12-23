import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict

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


def docker_network() -> str:
    in_docker = os.environ.get('_IN_DOCKER')
    if in_docker is not None:
        return 'sound-visualizer-testing-network'
    else:
        return 'bridge'


def in_docker() -> bool:
    in_docker = os.environ.get('_IN_DOCKER')
    return in_docker is not None


def docker_opts(port: int) -> Dict[str, Any]:
    opts: Dict[str, Any] = {'detach': True, 'remove': True, 'network': docker_network()}
    if not in_docker():
        # tests are run outside of docker, likely on a dev computer
        # in this case, we rely on port forwarding
        opts['ports'] = {port: port}
    return opts


def service_hostname(service_name: str) -> str:
    if in_docker():
        return service_name
    return 'localhost'
