#!/bin/bash
eval "$(conda shell.bash hook)"
read -p "Execute animation.py(Text Processing and Generating Skeleton)? (y/n): " skel_perm
if [ "$skel_perm" == "y" ]; then
    read -p "Write arguments (--text_file or --text_prompt): " args
    conda activate PriorMDM
    python animation.py "$args"
    conda deactivate
else
    echo "Skipping Skeleton Generation"
fi

read -p "Generate a video? (y/n): " video_perm

if [ "$video_perm" == "y" ]; then
    echo "Run Follow Your Pose"
    conda activate fupose
    python generate.py
    #cd /workspace/animation_from_TP/FollowYourPose
    #TORCH_DISTRIBUTED_DEBUG=DETAIL accelerate launch txt2video.py --config="/workspace/animation_from_TP/condition.yaml" --skeleton_path="/workspace/animation_from_TP/pose_video/soccer.mp4" --file_name="Dancing"
else
    echo "Stopping the program"
fi

