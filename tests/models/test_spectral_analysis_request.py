import pymongo
import pytest

import docker
from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)
from tests.util import docker_opts, service_hostname


@pytest.fixture(scope='module')
def mongo():
    client = docker.from_env()
    mongo_container = client.containers.run('mongo', name='mongo', **docker_opts(port=27017))
    yield mongo_container
    mongo_container.kill()


@pytest.fixture()
def mongo_client(mongo):
    return pymongo.MongoClient(service_hostname(mongo.name), 27017)


def test_should_load(mongo_client):
    orm = SpectralAnalysisFlowORM(mongo_client['dummy'])
    analysis = SpectralAnalysisFlow(
        id='foobar',
        status='REQUESTED',
        parameters=SpectralAnalysisParameters(overlap_factor=0.90, frame_size_power=12),
    )
    orm.save_request(analysis)

    assert orm.load_all_requests()[0] == analysis


def test_should_load_by_id(mongo_client):
    orm = SpectralAnalysisFlowORM(mongo_client['dummy'])
    analysis = SpectralAnalysisFlow(
        id='foobar',
        status='REQUESTED',
        parameters=SpectralAnalysisParameters(overlap_factor=0.90, frame_size_power=12),
    )
    orm.save_request(analysis)
    assert orm.load_request_by_id('foobar') == analysis
