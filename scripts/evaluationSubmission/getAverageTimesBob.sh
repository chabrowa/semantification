#!/bin/bash

echo -e  'Dataset \t Number of Files \t Total Time \t Average Time'

for file in $1
do
	echo -en $file'\t'
	awk '$3==100 && previous!=100 {print $10} {previous=$3}' $file | awk 'BEGIN {FS=":";OFS="\t"} {num++;time+=$3} END {print num,time,time/num}'
done