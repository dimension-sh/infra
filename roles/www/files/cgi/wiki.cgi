#!/usr/bin/env python3

from markdown.extensions.wikilinks import WikiLinkExtension
import markdown
import os
import cgi
import cgitb
cgitb.enable()


WIKI_ROOT = '/var/www/wiki/'
BAD_CHARACTERS = ['.', '/', '\\', ' ']

with open(os.path.join(WIKI_ROOT, 'template.html')) as fobj:
    template = fobj.read()

print('Content-Type: text/html')
print('')

# Get page name
qs = cgi.parse()
if 'p' in qs:
    page = qs['p'][0].lower()
else:
    page = 'index'

# Sanitize for bad filenames
for char in BAD_CHARACTERS:
    page = page.replace(char, '_')

# Check if the page exists
page_path = os.path.join(WIKI_ROOT, '%s.md' % page)
if not os.path.exists(page_path):
    page_path = os.path.join(WIKI_ROOT, '404.md')

# Open and format the page
with open(page_path, 'r') as fobj:
    page_data = fobj.read()
    html = markdown.markdown(page_data, extensions=[
                             'tables', WikiLinkExtension(base_url='/cgi/wiki.cgi?p=', end_url='')])

print(template.replace('<!--CONTENT-->', html))
