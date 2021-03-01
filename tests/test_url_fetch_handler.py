from io import BytesIO

import pytest
import werkzeug
from werkzeug.datastructures import MultiDict, FileStorage
from pdf_service import pdf_service

from pdf_service import URLFetchHandler
from pdf_service.errors import URLFetcherCalledAfterExitException


def test_exits_without_throwing_if_fetcher_isnt_called():
    with URLFetchHandler():
        pass


def test_throws_if_fetcher_throws():
    with pytest.raises(werkzeug.exceptions.Forbidden):
        with URLFetchHandler() as url_fetcher:
            # Swallow exception just like weasyprint
            # noinspection PyBroadException
            try:
                url_fetcher("https://example.com/test.png")
            except:
                pass



def test_throws_when_called_after_exit():
    handler = URLFetchHandler()
    with handler:
        pass

    with pytest.raises(URLFetcherCalledAfterExitException):
        handler("https://example.com/test.png")


def test_throws_bad_request_when_multiple_errors_happened():
    with pytest.raises(werkzeug.exceptions.BadRequest):
        with URLFetchHandler() as url_fetcher:
            # Swallow exception just like weasyprint
            # noinspection PyBroadException
            try:
                url_fetcher("https://example.com/test.png")
            except:
                pass

            # noinspection PyBroadException
            try:
                url_fetcher("test.png")
            except:
                pass


@pytest.fixture()
def request_context():
    with pdf_service.test_request_context():
        yield


@pytest.fixture()
def files_dict(request_context):
    yield MultiDict({
        'test.png': FileStorage(
            BytesIO(b'test img'),
            filename="test.png",
            name="test.png",
            content_type="image/png"
        )
    })


def test_resolves_local_url_with_leading_slash(files_dict):
    with URLFetchHandler(files_dict) as url_fetcher:
        result = url_fetcher("/test.png")
        assert result is not None
        assert result['file_obj'] == files_dict.get('test.png')


def test_resolves_local_url_without_leading_slash(files_dict):
    with URLFetchHandler(files_dict) as url_fetcher:
        result = url_fetcher("test.png")
        assert result is not None
        assert result['file_obj'] == files_dict.get('test.png')
