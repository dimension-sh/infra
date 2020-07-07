#!/usr/bin/env python3
# Updates the user page on the website with the current user list

import cgi
import pwd
import os.path
import sys

users = 0

sys.stdout.write('Content-Type: text/html\n\n')

sys.stdout.write("<ul>\n")
for user in sorted(pwd.getpwall(), key=lambda x: x.pw_name):
    # if the user doesn't have a public_html folder, skip
    if not os.path.exists(os.path.join(user.pw_dir, 'public_html')) or user.pw_gid != 100:
        continue

    # if .hidden exists in the public_html, skip it
    if os.path.exists(os.path.join(user.pw_dir, 'public_html', '.hidden')):
        continue

    gecos = ''
    if user.pw_gecos:
        gecos = ' - %s' % user.pw_gecos
    entry = "<li><a href='/~%s/'>~%s</a>%s</li>\n" % (user.pw_name, user.pw_name, gecos)
    users += 1
    sys.stdout.write(entry)

sys.stdout.write("</ul>\n")
sys.stdout.write("<p>Total Users: <b>%d</b></p>" % users)