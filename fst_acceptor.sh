#!/bin/sh
# author: Erica Sim
#$1 is fst file name
#$2 is input file

while read curr; do
    RESULT="$(echo $curr | carmel -kOE 1 -sli $1 2>&1 | tail -n 1)"
    if [[ $RESULT = "0" ]]
    then 
        echo "$curr => *none* 0"
    else
        echo "$curr => $RESULT"
    fi
done < $2