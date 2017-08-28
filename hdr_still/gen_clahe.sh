#!/bin/bash

# In each directory, create a clahe for std.jpg and hdr.jpd

for dir in $(ls stills);
do
    dir="stills/$dir"
    echo $dir

    # std
    if !(ls $dir | grep -q std_clahe)
    then
        python cv_clahe.py ${dir}/std.jpg
    fi

    # hdr
    if !(ls $dir | grep -q hdr_clahe)
    then
        python cv_clahe.py ${dir}/hdr.jpg
    fi

done
