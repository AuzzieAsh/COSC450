#!/bin/bash

echo "k-means++, HSV, Cluster, khc (2 1 1)" >> cluster_output.txt

PDIR=penguin
SDIR=khc
FILE_IN=images/$PDIR.jpeg

mkdir results/$PDIR
mkdir results/$PDIR/$SDIR

i=0
while [ $i -lt 10 ]; do
    FILE_OUT=results/$PDIR/$SDIR/khc_out$i.png
    ./asgn2 $FILE_IN $FILE_OUT 10 2 1 1 0
    let i=i+1
done
