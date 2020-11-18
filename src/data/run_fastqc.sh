#!/bin/sh
mkdir -p "$3"
for i in $(ls $1*.gz | head -$2); 
do /opt/FastQC/fastqc "$i" -o "$3";
done;
