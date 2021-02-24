import pytest

from pdfminer import high_level
from pdf_service import pdf_service
from pdf2image import convert_from_bytes
from pathlib import Path
import tempfile
from io import BytesIO
from diffimg import diff


# Tests the basic (non multipart) API

@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_responds(client):
    rv = client.post('/generate', data="<p>Test text in PDF</p>", content_type="application/json")
    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type


def test_contains_text(client):
    rv = client.post('/generate', data="<p>Test text in PDF</p>", content_type="application/json")

    file = BytesIO(rv.data)
    text = high_level.extract_text(file)

    assert 'Test text in PDF' in text


def test_matches_visually(client):
    rv = client.post('/generate', data="<p>Test text in PDF</p>", content_type="application/json")

    temp = tempfile.mkdtemp()
    paths = convert_from_bytes(rv.data,
                               output_file="basic_",
                               output_folder=temp,
                               fmt="png",
                               paths_only=True)

    base = Path(__file__).parent.joinpath("test-data")
    original_files = base.glob("basic_*.png")
    assert sum(1 for _ in original_files) == len(paths), "Number of generated pages differs from " \
                                                         "expected "

    for expected, actual in zip(base.glob("basic_*.png"), paths):
        percentage = diff(expected, actual) * 100
        assert percentage == 0.0, "Rasterized page differs from expected result by more than the " \
                                  "allowed threshold "
