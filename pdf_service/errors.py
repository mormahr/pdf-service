class URLFetcherCalledAfterExitException(Exception):
    def __init__(self):
        self.message = "Called URLFetchCather after it was closed."
