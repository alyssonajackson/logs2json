#!/bin/bash

test -z "$1" && echo "missing input log file" && exit 1

dir="$(dirname $0)"

python $dir/apache/main.py -f "$1" $2
