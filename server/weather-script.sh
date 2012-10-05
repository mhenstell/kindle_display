#!/bin/sh

cd "$(dirname "$0")"
set -e

WUND_CREDS=`grep WUNDERGROUND_KEY settings.conf | awk -F"=" '{print $2}'`
IMAGE_PATH=`grep SERVER_IMAGE_PATH settings.conf | awk -F"=" '{print $2}'`
ZIP=`grep ZIP_CODE settings.conf | awk -F"=" '{print $2}'`

python2 weather-script.py $WUND_CREDS $ZIP
rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg
pngcrush -c 0 -ow weather-script-output.png
cp -f weather-script-output.png $IMAGE_PATH/weather-script-output.png
