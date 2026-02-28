class FileNotFoundError(Exception):
    pass


class LinkExpiredError(Exception):
    pass


class DownloadLimitReachedError(Exception):
    pass


class InvalidExpiryError(Exception):
    pass


class InvalidDownloadLimitError(Exception):
    pass