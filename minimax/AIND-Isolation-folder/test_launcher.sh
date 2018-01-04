#!/bin/bash
# ((var = 0))
echo "Running the software"
var=1

for i in {1..100}; do
	((other_var=$var+1))
	out_file="./output_files/out_"
	out_file+=$var
	out_file+=".txt"
	out_file_other="./output_files/out_"
	out_file_other+=$other_var
	out_file_other+=".txt"
	echo $var
	echo $other_var
	python3 tournament.py > $out_file & python3 tournament.py > $out_file_other
	((var += 2))
done 2>/dev/null