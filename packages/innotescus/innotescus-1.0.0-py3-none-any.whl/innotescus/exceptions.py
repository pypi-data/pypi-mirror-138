class YankedVersionError(RuntimeError):
    """ Raised when a version of the client is no longer supported and
    must be updated.
    """
    def __init__(self, reason):
        super().__init__(f'Your innotescus version is not supported and must be updated: {reason}')
