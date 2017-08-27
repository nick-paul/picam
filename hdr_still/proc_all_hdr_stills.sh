#!/bin/bash

for dir in $(ls stills);
do
    dir="stills/$dir"
    if !(ls $dir | grep -q hdr)
    then
        ./proc_hdr $dir/cap*
    fi


done
