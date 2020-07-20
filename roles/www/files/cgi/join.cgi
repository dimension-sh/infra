#!/usr/bin/env python3

import sys
import cgi
import re
import struct
import binascii
import base64
import pwd
import os.path
import ipaddress
import dns.resolver

REQUESTS_FOLDER = '/var/www/requests'

VALID_SSH_KEYTYPES = [
    'sk-ecdsa-sha2-nistp256@openssh.com',
    'ecdsa-sha2-nistp256',
    'ecdsa-sha2-nistp384',
    'ecdsa-sha2-nistp521',
    'sk-ssh-ed25519@openssh.com',
    'ssh-ed25519',
    'ssh-rsa',
]

def validate_ip_dnsbl(ip):
    """Validate a IP against DroneBL"""
    resolv = dns.resolver.Resolver()

    # Check the IP address
    try:
        ipobj = ipaddress.ip_address(ip)
    except ValueError:
        return False

    # Generate the query
    if isinstance(ipobj, ipaddress.IPv4Address):
        query = ipobj.reverse_pointer.replace('.in-addr.arpa', '.dnsbl.dronebl.org')
        query_type = 'A'
    elif isinstance(ipobj, ipaddress.IPv6Address):
        query = ipobj.reverse_pointer.replace('.ip6.arpa', '.dnsbl.dronebl.org')
        query_type = 'AAAA'
    else:
        return False

    # Query
    try:
        resolv.query(query, query_type)
        return False
    except dns.resolver.NXDOMAIN:
        pass
    return True


def validate_username(username):
    if re.match(r"^[a-z][-a-z0-9]*$", username) is None:
        return False
    if os.path.exists(os.path.join(REQUESTS_FOLDER, 'banned_usernames.txt')):
        with open(os.path.join(REQUESTS_FOLDER, 'banned_usernames.txt'), 'r') as fobj:
            if username in [x.strip() for x in fobj.readlines() if x.strip() != '']:
                return False
    return True


def validate_sshkey(keystring):
    """ Validates that SSH pubkey string is valid """
    # do we have 3 fields?
    fields = len(keystring.split(' '))
    if fields < 2 or fields > 3:
        return 'Incorrect number of fields (%d)' % fields

    if fields == 2:
        keytype, pubkey = keystring.split(' ')
    if fields == 3:
        keytype, pubkey, _ = keystring.split(' ')

    # Check it is a valid type
    if not keytype in VALID_SSH_KEYTYPES:
        return 'Invalid keytype'

    # Decode the key data from Base64
    try:
        data = base64.decodebytes(pubkey.encode())
    except binascii.Error:
        return 'Error decoding the pubkey'

    # Get the length from the data
    try:
        str_len = struct.unpack('>I', data[:4])[0]
    except struct.error:
        return 'Error aquiring key length'

    # Keytype is encoded and must match
    if not data[4:4+str_len].decode('ascii') == keytype:
        return 'Embedded keytype does not match declared keytype (%s vs %s)' % (data[4:4+str_len].decode('ascii'), keytype)
    return True


def validate_email(address):
    """ QUickly validates a email address, nowhere near perfect, but good enough """
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", address) != None


def error(msg):
    print('<meta http-equiv="refresh" content="3; URL=\'http://dimension.sh/join.html\'"/>')
    print('<p>An error was encountered: %s</p>' % msg)


def main():
    sys.stdout.write('Content-Type: text/html\n\n')

    # Get the form and extract the values
    form = cgi.FieldStorage()
    username = form.getvalue('username')
    email = form.getvalue('email')
    ssh_key = form.getvalue('ssh_key')
    why = form.getvalue('why')

    if not validate_ip_dnsbl(os.environ["REMOTE_ADDR"]):
        error('Sorry, IP no bueno.')
        return

    if not username or not email or not ssh_key or not why:
        error('All fields must be provided.')
        return

    if not validate_username(username) is True:
        error('Invalid username')
        return

    if not validate_sshkey(ssh_key) is True:
        error('Invalid SSH public key')
        return

    if not validate_email(email):
        error('Invalid email address provided')
        return

    try:
        if pwd.getpwnam(username):
            error('Username %s is already took' % username)
            return
    except KeyError:
        pass

    with open(os.path.join(REQUESTS_FOLDER, username), 'w') as fobj:
        fobj.write('Why\n---\n\n%s\n\n# mkuser %s %s "%s"\n' %
                   (why.replace('\n', ' '), username, email, ssh_key))

    print('<meta http-equiv="refresh" content="0; URL=\'http://dimension.sh/join_submitted.html\'"/>')


if __name__ == '__main__':
    main()
