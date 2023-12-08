#!/bin/bash
eval "$(conda shell.bash hook)"

conda activate mdm
python single_animation.py --text_file=./input_prompt.txt
conda deactivate


