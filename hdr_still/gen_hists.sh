#!/bin/bash

# In each directory, create a hist
for dir in $(ls stills);
do
    dir="stills/$dir"
    echo $dir
    if !(ls $dir | grep -q hist)
    then
        python cv_hist.py ${dir}/*
    fi
done
