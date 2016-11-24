"""Exception specifications for clChecker"""


class WhoisConnectionError(Exception):
    """
    An Exception for when the whois connection failed.
    """


class InvalidDomain(Exception):
    """
    An Exception to denote that the domain is invalid.
    """


class WhoisServerNotResponding(Exception):
    """
    An Exception to denote that NIC.cl whois server is not responding us.
    """