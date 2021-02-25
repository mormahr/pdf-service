import werkzeug


class ForbiddenURLFetchError(werkzeug.exceptions.HTTPException):
    code = 403

    def __init__(self, url):
        self.message = "Attempted to fetch forbidden url (%r)" % url
