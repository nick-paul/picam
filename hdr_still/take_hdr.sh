#!/bin/bash

# Set up variables
WIDTH=1920
HEIGHT=1080
TIMEOUT=1500
NOW=$(date +"%m_%d_%y__%H_%M_%S")

# Camera parameters
ISO=(100 100 200 400) # ISO
SS=(1 300 2000 15000) # Shutter Speed

# Create the directory to store the images
mkdir -p stills/${NOW}

# Take an autoexposure image
raspistill -w $WIDTH -h $HEIGHT -o stills/${NOW}/std.png --timeout $TIMEOUT

# Take manual exposure shots
COUNTER=0
while [ $COUNTER -lt 4 ];
do
    ISO_I=${ISO[$COUNTER]}
    SS_I=${SS[$COUNTER]}
    raspistill -w $WIDTH -h $HEIGHT -ISO $ISO_I -ss $SS_I -o stills/${NOW}/cap_iso${ISO_I}_ss_${SS_I}.png --timeout $TIMEOUT
    let COUNTER=COUNTER+1
done

echo "Done!"
