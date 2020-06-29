#!/usr/bin/env python3

import cgi
import re
import struct
import binascii
import base64
import pwd

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
    if not keytype in ['ssh-rsa', 'ssh-ed25519']:
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
    print('<meta http-equiv="refresh" content="1; URL=\'http://dimension.sh/join.html\'"/>')
    print('<p>An error was encountered: %s</p>' % msg)

def main():
    # Get the form and extract the values
    form = cgi.FieldStorage()
    username = form.getvalue('username')
    email = form.getvalue('email')
    ssh_key = form.getvalue('ssh_key')
    why = form.getvalue('why')

    if not username or not email or not ssh_key or not why:
        error('All fields must be provided')
        return

    if not validate_sshkey(ssh_key) is True:
        error('Invalid SSH key')
        return

    if not validate_email(email):
        error('Invalid email address provided')
        return

    if pwd.getpwnam(username):
        error('Username %s is already took' % username)
        return

    with open('/var/www/requests/%s' % username) as fobj:
        fobj.write('%s\n\n mkuser %s %s "%s"' % (why.replace('\n', ' '), username, email, ssh_key))

    print('<p>Your request has been submitted</p>')

if __name__ == '__main__':
    main()