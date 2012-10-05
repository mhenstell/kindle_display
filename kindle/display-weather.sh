#!/bin/sh

cd "$(dirname "$0")"

rm weather-script-output.png
#eips -c
#eips -c

if wget $1; then
	eips -g weather-script-output.png
else
	eips -g weather-image-error.png
fi
