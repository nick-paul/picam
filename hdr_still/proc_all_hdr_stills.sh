#!/bin/bash

# In each directory, create an hdr image
for dir in $(ls stills);
do
    dir="stills/$dir"

    # Only create hdr image if the folder doen't
    # already contain one
    if !(ls $dir | grep -q hdr)
    then
        ./proc_hdr $dir/cap*
    fi

done
