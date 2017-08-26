#!/bin/bash

TIMEOUT=2000

NOW=$(date +"%m_%d_%y__%H_%M_%S")
mkdir -p stills/${NOW}

raspistill -w 320 -h 240 -o stills/${NOW}/std.png --timeout $TIMEOUT

ISO=(100 200 400 800)
SS=(6000 600 100 20)
COUNTER=0
while [ $COUNTER -lt 4 ];
do
    ISO_I=${ISO[$COUNTER]}
    SS_I=${SS[$COUNTER]}
    raspistill -w 320 -h 240 -ISO $ISO_I -ss $SS_I -o stills/${NOW}/cap_iso${ISO_I}_ss_${SS_I}.png --timeout $TIMEOUT
    let COUNTER=COUNTER+1
done
