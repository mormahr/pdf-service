import pytest

from pdf_service import pdf_service

@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_responds(client):
    rv = client.get('/health')
    assert 200 == rv.status_code
    assert b"Healthy" == rv.data
