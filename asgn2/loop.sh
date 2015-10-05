#!/bin/bash

PDIR=penguin
SDIR=kh2
FILE_IN=images/$PDIR.jpeg
K=8
C=1
D=1
OUTPUT="K: $K C: $C D: $D"

echo $OUTPUT >> cluster_output.txt

mkdir results/$PDIR
mkdir results/$PDIR/$SDIR

i=0
while [ $i -lt 10 ]; do
    FILE_OUT=results/$PDIR/$SDIR/sr_out$i.png
    ./asgn2 $FILE_IN $FILE_OUT $K $C $D 1 0
    let i=i+1
done
