#!/bin/bash

if [[ ! $(pgrep -f bmeweather.py) ]]; then
    /usr/bin/python /home/dietpi/pyweather/bmeweather.py &
    echo "starting logger"
fi

