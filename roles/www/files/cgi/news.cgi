#!/bin/bash

FILE=`find /srv/news/ -name '*.md' | sort -r | head -1`

echo "Content-Type: text/plain"
echo ""
/usr/local/bin/news2md $FILE | pandoc -t html5 --ascii