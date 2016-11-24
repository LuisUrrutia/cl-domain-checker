#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""clChecker main application setup code."""

# Third-party imports
import socket
import re

# Application imports
from clchecker.exception import ConnectionError

# Regexp to match with server response
who = re.compile(r"\)\n+(\S.*\S)")
expiration = re.compile(r"Exp.*date.*?(\d.*)")
administrative = re.compile(r"Administrative.*\n.*Nombre\s+:\s+(.*)\n.*ón:\s(.*)")
technical = re.compile(r"Technical.*\n.*Nombre\s+:\s+(.*)\n.*ón:\s(.*)")


def check(domain):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("whois.nic.cl", 43))
    except:
        raise ConnectionError("Can't connect to NIC.cl WHOIS server.")

    sock.send(("%s\r\n" % domain).encode("utf-8"))

    buff = b''
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        buff += data

    if b'no existe' in buff:
        return None

    str_buff = buff.decode("latin-1")

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


