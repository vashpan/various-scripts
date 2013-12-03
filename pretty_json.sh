#!/bin/bash

# Pretty JSON, beautify JSON given in input to output.

ME=`basename $0`
if [ $# -eq 2 ] 
	then
	cat $1 | python -mjson.tool > $2
	exit 
fi

echo "Usage: ./$ME <in.json> <out.json>"
