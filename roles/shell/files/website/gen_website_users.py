#!/usr/bin/env python3
# Updates the user page on the website with the current user list

import pwd
import os.path

users = 0
with open('/var/www/dimension.sh/inc/users.gen.html', 'w') as fobj:
  fobj.write("<ul>\n")
  for user in pwd.getpwall():

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
    fobj.write(entry)
  fobj.write("</ul>\n")
  fobj.write("<p>Total Users: <b>%d</b></p>" % users)