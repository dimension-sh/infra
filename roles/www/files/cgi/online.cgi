#!/bin/bash

ONLINE=$(who | cut -d " " -f 1 | sort | uniq | wc -l)

echo "Content-Type: text/plain"
echo ""
echo $ONLINE
