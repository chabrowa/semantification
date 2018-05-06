#!/bin/bash

echo -e  'Dataset \t Number of Files \t Total Time \t Average Time'

for file in $1
do
	echo -en $file'\t'
	awk 'BEGIN {OFS="\t"} {num++;total+=$4} END {print num,total,total/num}' $file
done