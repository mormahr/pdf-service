import pytest

from pdf_service import pdf_service
from pdf2image import convert_from_bytes
from pathlib import Path
import tempfile
from diffimg import diff


@pytest.fixture
def client():
    with pdf_service.test_client() as client:
        yield client


def resolve_all_tests():
    base = Path(__file__).parent.joinpath("../test-data")
    return [file.stem.replace(".html", "") for file in base.glob("*.html")]


@pytest.mark.parametrize("name", resolve_all_tests())
def test_matches_visually(client, name):
    base = Path(__file__).parent.joinpath("../test-data")

    if base.joinpath(name).exists():
        data = {
            'index.html': (base.joinpath(name + ".html").open('rb'), 'index.html', 'text/html'),
        }

        for file in base.joinpath(name).iterdir():
            data[file.name] = (file.open('rb'), file.name, 'image/png')

        rv = client.post('/generate', data=data, content_type="multipart/form-data")
    else:
        html = base.joinpath(name + ".html").read_text()
        rv = client.post('/generate', data=html, content_type="text/html")

    assert 200 == rv.status_code

    temp = tempfile.mkdtemp()
    paths = convert_from_bytes(rv.data,
                               output_file=name + "_",
                               output_folder=temp,
                               fmt="png",
                               paths_only=True)

    original_files = base.glob(name + "_*.png")
    assert sum(1 for _ in original_files) == len(paths), "Number of generated pages differs from " \
                                                         "expected "

    for expected, actual in zip(base.glob(name + "_*.png"), paths):
        percentage = diff(expected, actual, diff_img_file=tempfile.mktemp(".png")) * 100
        assert percentage == 0.0, "Rasterized page differs from expected result by more than the " \
                                  "allowed threshold "
