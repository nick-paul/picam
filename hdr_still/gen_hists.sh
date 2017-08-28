#!/bin/bash

CLAHE_HIST_FILES=(std.jpg hdr.jpg std_clahe.jpg hdr_clahe.jpg)
CV_HIST_PY=$(realpath cv_hist.py)

# In each directory, create a hist
for dir in $(ls stills);
do
    dir="stills/$dir"
    echo $dir

    # Standard histogram
    if !(ls $dir | grep -q hist.jpg)
    then
        olddir=$(pwd)
        cd $dir
        imgs=$(ls . | grep 'hdr.jpg\|std.jpg\|cap_*')
        python $CV_HIST_PY hist.png ${imgs}
        cd $olddir
    fi

    # clahe histogram
    if !(ls $dir | grep -q hist_clahe.jpg)
    then
        olddir=$(pwd)
        cd $dir
        python $CV_HIST_PY hist_clahe.png ${CLAHE_HIST_FILES[*]}
        cd $olddir
    fi
    
done
