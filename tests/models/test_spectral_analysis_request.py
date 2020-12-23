import pymongo
import pytest

from sound_visualizer.models.spectral_analysis_parameters import SpectralAnalysisParameters
from sound_visualizer.models.spectral_analysis_request import (
    SpectralAnalysisFlow,
    SpectralAnalysisFlowORM,
)
from tests.util import start_container


@pytest.fixture(scope='function')
def mongo():
    service = start_container(image='mongo', service_port=27017)
    yield service
    service.container.kill()


@pytest.fixture()
def mongo_client(mongo):
    return pymongo.MongoClient(mongo.host, mongo.port)


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
