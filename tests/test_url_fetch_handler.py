import pytest
import werkzeug

from pdf_service import URLFetchHandler
from pdf_service.errors import URLFetcherCalledAfterExitException


def test_exits_without_throwing_if_fetcher_isnt_called():
    with URLFetchHandler():
        pass


def test_throws_if_fetcher_throws():
    with pytest.raises(werkzeug.exceptions.Forbidden):
        with URLFetchHandler() as url_fetcher:
            url_fetcher("https://example.com/test.png")


def test_throws_when_called_after_exit():
    handler = URLFetchHandler()
    with handler:
        pass

    with pytest.raises(URLFetcherCalledAfterExitException):
        handler("https://example.com/test.png")
