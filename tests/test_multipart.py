from pathlib import Path

import pytest
from flask.testing import Client

from pdfminer import high_level

from pdf_service import pdf_service
from io import BytesIO


@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_responds(client: Client):
    data = {
        'index.html': (BytesIO(bytes('<p>Test text in PDF</p>', 'utf8')), 'index.html', 'text/html')
    }

    rv = client.post('/generate', data=data)
    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type


def test_contains_text(client):
    data = {
        'index.html': (BytesIO(bytes('<p>Test text in PDF</p>', 'utf8')), 'index.html', 'text/html')
    }

    rv = client.post('/generate', data=data)

    file = BytesIO(rv.data)
    text = high_level.extract_text(file)

    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type
    assert 'Test text in PDF' in text


def test_renders_external_resource(client: Client):
    data = {
        'index.html': (
            BytesIO(bytes('<p>Test <img src="/test.png"/></p>', 'utf8')),
            'index.html',
            'text/html'),
        'test.png': (
            Path(__file__).parent.joinpath('../test-data/assets/test.png').open('rb'),
            'test.png',
            'image/png'
        )
    }

    rv = client.post('/generate', data=data)
    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type
