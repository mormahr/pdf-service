import pytest

from pdf_service import pdf_service


@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_prohibit_external_url_fetches(client):
    rv = client.post('/generate',
                     data="<img src='https://example.com/test.png' />",
                     content_type="application/html")

    assert 403 == rv.status_code
