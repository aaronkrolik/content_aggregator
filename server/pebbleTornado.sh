#!/bin/sh

case "$1" in
    start)
        python tornadoToSolr.py 2>&1 > ~/pebble-logs/pebble.log &
        ;;
    stop)
        pkill -f tornadoToSolr.py
        ;;
esac
