#!/bin/sh

cd "$(dirname "$0")"

python2 test.py
rsvg-convert --background-color=white -o test-output.png test-output.svg
pngcrush -c 0 -ow test-output.png
cp -f test-output.png /Users/max/Sites/test-output.png
