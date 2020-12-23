import os
import random
import time
from datetime import datetime, timedelta
from typing import Any, Dict
from uuid import uuid4

import numpy as np
from docker.models.containers import Container
from promise import Promise

import docker


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
    # this env var is set by the docker file. maybe there is a cleaner way to do this ?
    in_docker = os.environ.get('_IN_DOCKER')
    if in_docker is not None:
        return 'sound-visualizer-testing-network'
    else:
        return 'bridge'


def in_docker() -> bool:
    in_docker = os.environ.get('_IN_DOCKER')
    return in_docker is not None


def docker_opts(host_port: int, service_port: int) -> Dict[str, Any]:
    opts: Dict[str, Any] = {'detach': True, 'remove': True, 'network': docker_network()}
    if not in_docker():
        # tests are run outside of docker, likely on a dev computer
        # in this case, we rely on port forwarding
        opts['ports'] = {service_port: host_port}
    return opts


class Service:
    def __init__(self, container: Container, host: str, port: int):
        self.container = container
        self.host = host
        self.port = port


def random_port() -> int:
    return random.randint(2000, 3000)


def start_container(image: str, service_port: int) -> Service:
    client = docker.from_env()
    port = random_port()
    id = uuid4().hex
    container = client.containers.run(
        image,
        name=f'{image[0:image.find(":")]}-{id}',
        **docker_opts(service_port=service_port, host_port=port),
    )
    if in_docker():
        return Service(container=container, host=container.name, port=service_port)
    else:
        return Service(container=container, host='localhost', port=port)
