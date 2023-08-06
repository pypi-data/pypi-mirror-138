class CiteprocException(Exception):
    """General, unspecific exception of md_citeproc"""
    pass


class CiteprocBinaryException(CiteprocException):
    """Exception concerning the citeproc-cli executable"""
    pass


class CiteprocStrictException(CiteprocException):
    """Warning converted to exception in strict mode"""
    pass


class CiteprocConfigException(CiteprocException):
    """Something went wrong during configuration of the exception"""
    pass
