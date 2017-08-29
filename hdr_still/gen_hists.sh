#!/bin/bash

echo "------ [ begin gen_hists.sh ] -------"

HELP_TEXT='gen_hists allhdr|clahe|stdhdr img|noimg png|eps'

if [ $# -lt 3 ];
then
    echo "needs 3 arguments"
    echo $HELP_TEXT
    exit 1
fi

TYPE=$1 #allhdr, clahe, stdhdr


if [ $2 == img ];
then
    echo "using img"
    SHOW_IMG=true
elif [ $2 == noimg ];
then
    echo "not using img"
    SHOW_IMG=false
else
    echo "invalid second arg: $2"
    echo $HELP_TEXT
    exit 1
fi

if [ $3 == png ];
then
    echo "filetype: png"
    FILETYPE=png
elif [ $3 == eps ];
then
    echo "filetype: eps"
    FILETYPE=eps
else
    echo "invalid filetype: $3"
    echo $HELP_TEXT
    exit 1
fi


CLAHE_HIST_FILES=(std.jpg hdr.jpg std_clahe.jpg hdr_clahe.jpg)
STD_HDR_HIST_FILES=(std.jpg hdr.jpg)

FIGNAME="hist_$TYPE"

# Python file to use
if [ $SHOW_IMG == true ];
then
    CV_HIST_PY=$(realpath cv_hist_img.py)
    FIGNAME="${FIGNAME}_img"
else
    CV_HIST_PY=$(realpath cv_hist.py)
fi

FIGNAME="${FIGNAME}.${FILETYPE}"

if [ $TYPE == allhdr ];
then
    # var will be set in loop
    :
elif [ $TYPE == clahe ];
then
    IMG_FILES=${CLAHE_HIST_FILES[*]}
elif [ $TYPE == stdhdr ];
then
    IMG_FILES=${STD_HDR_HIST_FILES[*]}
else
    echo $HELP_TEXT
    exit 1
fi



# In each directory, create a hist
for dir in $(ls stills);
do
    dir="stills/$dir"
    echo ">> $dir"

    # change into dir
    olddir=$(pwd)
    cd $dir

    # image files
    if [ $TYPE == allhdr ];
    then
        imgs=$(ls . | grep 'hdr.jpg\|std.jpg\|cap_*')
    else
        imgs=$IMG_FILES
    fi

    echo "Using img files: " $imgs

    # only run command if file does not exist
    if !(ls . | grep -q $FIGNAME)
    then
        python $CV_HIST_PY $FIGNAME ${imgs}
    fi

    cd $olddir

done
