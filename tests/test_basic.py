import pytest

from pdfminer import high_level
from pdf_service import pdf_service
from io import BytesIO


# Tests the basic (non multipart) API

@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_responds(client):
    rv = client.post('/generate', data="<p>Test text in PDF</p>", content_type="text/html")
    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type


def test_contains_text(client):
    rv = client.post('/generate', data="<p>Test text in PDF</p>", content_type="text/html")

    file = BytesIO(rv.data)
    text = high_level.extract_text(file)

    assert 'Test text in PDF' in text
