import pytest

from pdfminer import high_level
from pdf_service import pdf_service
from io import BytesIO
from pdf_service.data_uri import parse
from pdf_service.errors import InvalidDataURI


# Tests the data URI support

@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def test_contains_text(client):
    rv = client.post('/generate',
                     data="<img width=\"200\" height=\"200\" alt=\"\" "
                          "src=\"data:image/svg+xml;base64,"
                          "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdwb3J0PSIwIDAg"
                          "MjAwIDIwMCIgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiPjx0ZXh0IHg9IjAiIHk9IjIwIj5T"
                          "VkcgZGF0YS11cmk8L3RleHQ+PC9zdmc+\" />",
                     content_type="text/html")

    assert 200 == rv.status_code
    assert 'application/pdf' == rv.content_type

    file = BytesIO(rv.data)
    text = high_level.extract_text(file)

    assert 'SVG data-uri' in text


def test_invalid_data_uri(client):
    t = "data:*garbled*;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6" \
        "eSBkb2cu"
    with pytest.raises(InvalidDataURI):
        parse(t)


def test_non_base64_data_uri(client):
    t = "data:text/plain;charset=utf-8,sample"
    (_, _, _, _, text) = parse(t)

    assert text == "sample"

