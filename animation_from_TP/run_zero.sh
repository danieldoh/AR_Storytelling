#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate T2VZeroNew
python ../Text2Video-Zero/run.py --text_file="./input_prompt.txt"
conda deactivate

