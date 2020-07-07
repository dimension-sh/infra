#!/bin/bash

mkdir -p /tmp/news
chmod 0700 /tmp/news

FILE=$(find /srv/news/ -name '*.md' | sort -r | head -1)
FILEHASH=$(echo $FILE | sha256sum | cut -d " " -f 1)

if [ ! -f "/tmp/news/${FILEHASH}" ]; then
    /usr/local/bin/news2md $FILE | pandoc -t html5 --ascii >"/tmp/news/${FILEHASH}"
fi

echo "Content-Type: text/plain"
echo ""
cat "/tmp/news/${FILEHASH}"
