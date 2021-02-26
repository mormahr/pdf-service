import werkzeug
from sentry_sdk import add_breadcrumb

from .errors import ForbiddenURLFetchError, URLFetcherCalledAfterExitException


class URLFetchHandler:
    """
    Implements an url_fetcher for WeasyPrint.
    Normally WeasyPrint will swallow any url fetch errors and demote them to warning.
    This implementation keeps track of thrown errors and throws an exception if any occured.

    It's important to note that the `url_fetcher` is stored by HTML and will then be used by the
     `.render` method, so the render call has to be inside the with, too.

    :raise: werkzeug.exceptions.Forbidden() if a forbidden URL was requested.

    :example:
    >>> from weasyprint import HTML
    >>>
    >>> with URLFetchHandler() as url_fetcher
    >>>   html = HTML(string=html_string, url_fetcher=url_fetcher)
    >>>   doc = html.render()
    """

    def __init__(self):
        self.url_errors = []
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        if len(self.url_errors) != 0:
            raise werkzeug.exceptions.Forbidden()

    def __call__(self, url):
        if self.closed:
            raise URLFetcherCalledAfterExitException()

        error = ForbiddenURLFetchError(url)
        add_breadcrumb(message="Refused to fetch URL (%s)" % url)
        self.url_errors.append(error)
        raise error
