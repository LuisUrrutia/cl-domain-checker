#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""clChecker main application setup code."""

# Third-party imports
import socket
import re

# Application imports
from clchecker.exception import WhoisConnectionError
from clchecker.exception import InvalidDomain

# Regexp to check if domain is valid
domain_checker = re.compile(r"[0-9a-zñáéíóú]+\.cl$", re.IGNORECASE)

# Regexp to match with server response
who = re.compile(r"\)\n+(\S.*\S)")
expiration = re.compile(r"Exp.*date.*?(\d.*)")
administrative = re.compile(r"Administrative.*\n.*Nombre\s+:\s+(.*)\n.*ón:\s(.*)")
technical = re.compile(r"Technical.*\n.*Nombre\s+:\s+(.*)\n.*ón:\s(.*)")


def check(domain, info=False):
    """Check if a domain is registered or not, with info about it if is required.

    :param domain: A domain name to check, it must be a .cl domain.
    :param info: Return info about the domain if its registered.
    :return: A boolean or False/Dict if info param is True.
    """
    buffer = whois(domain)

    if b'no existe' in buffer:
        return False

    if info:
        return _parse_whois_data(buffer)

    return True


def whois(domain):
    """Performs a whois lookup with NIC.cl whois server.

    :param domain: Domain name to perform a lookup.
    :return: Bytes literals with info about the domain.
    """
    if not _is_valid_domain(domain):
        raise InvalidDomain("The domain must be a valid .cl TLD.")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("whois.nic.cl", 43))
    except:
        raise WhoisConnectionError("Can't connect to NIC.cl WHOIS server.")

    sock.settimeout(5.0)
    sock.send(("%s\r\n" % domain).encode("utf-8"))

    buff = b''
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        buff += data

    return buff


def _is_valid_domain(domain):
    """Check if the domain is a valid .cl TLD.

    :param domain: The domain to check.
    :return: Boolean
    """
    if domain_checker.match(domain) is not None:
        return True
    return False


def _parse_whois_data(buffer):
    """Parse the data obtained through a whois lookup.

    :param buffer: Bytes literals with info about the domain.
    :return: Dictionary with the parsed info.
    """
    str_buff = buffer.decode("latin-1")

    try:
        who_match = who.search(str_buff).group(1)
    except AttributeError:
        who_match = ''

    try:
        exp_match = expiration.search(str_buff).group(1)
    except AttributeError:
        exp_match = ''

    try:
        administrative_matches = administrative.search(str_buff)

        administrative_name_match = administrative_matches.group(1)
        administrative_organization_match = administrative_matches.group(2)
    except AttributeError:
        administrative_name_match = ''
        administrative_organization_match = ''

    try:
        technical_matches = technical.search(str_buff)

        technical_name_match = technical_matches.group(1)
        technical_organization_match = technical_matches.group(2)
    except AttributeError:
        technical_name_match = ''
        technical_organization_match = ''

    return {
        'owner': who_match,
        'expires': exp_match,
        'administrative_name': administrative_name_match,
        'administrative_organization': administrative_organization_match,
        'technical_name': technical_name_match,
        'technical_organization': technical_organization_match
    }
