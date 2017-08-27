#!/bin/bash

for f in $(ls stills/*/*.png);
do
    mv "$f" "${f%.png}.jpg"
done
