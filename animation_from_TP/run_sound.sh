#!/bin/bash
eval "$(conda shell.bash hook)"

filename="/workspace/animation_from_TP/sound.txt"
#filename=$1

if [ ! -f "$filename" ]; then
    echo "File not found: $filename"
    exit 1
fi

line_count=0
while read -r line; do
    ((line_count++))
done < "$filename"

echo "Line number is $line_count"

if [ $line_count == 0 ]; then
    echo "No prompt in file"
elif [ $line_count == 1 ]; then
    echo "1"
    conda activate music
    python music.py --text_file=./sound.txt
    conda deactivate
#else
#    echo "more than 1"
#    conda activate PriorMDM
#    python multi_animation.py --text_file=./input_prompt.txt
#    conda deactivate
fi
conda deactivate

