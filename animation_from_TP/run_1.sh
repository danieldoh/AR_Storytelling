#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate PriorMDM
python multi_animation.py --text_file=./input_prompt.txt
conda deactivate

echo "Run Follow Your Pose"
conda activate fupose
python generate_1.py

