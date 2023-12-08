import os
import re
import cv2
import argparse
import yaml
import spacy
import subprocess


def run_follow(model, condition_list):
    #for cond in condition_list:
    #print("/workspace/animation_from_TP/pose_video/[    ]/[    ]\n")
    #pose_folder = input("Please provide pose folder name: ")
    #pose_name = input("Please provide pose video name(e.g., [action]_0[0/1/2].mp4): ")
    posepath = os.path.join("/workspace/animation_from_TP/static/pose_video/skel", "skel_01.mp4")
    if not(os.path.exists(posepath)):
        raise FileNotFoundError(f"{posepath}: No directory \n")
        #pose_folder = input("Please provide pose folder name: ")
        #pose_name = input("Please provide pose video name(e.g., [action]_0[0/1/2].mp4): ")
        #posepath = os.path.join("/workspace/animation_from_TP/pose_video", pose_folder, pose_name)
    cap = cv2.VideoCapture(posepath)
    num_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_len = num_frame // 5
    print(video_len)
    info_updated = {}
    print(f"\"{condition_list[0]}\" is processing")
    with open("./condition.yaml") as rf:
        info = yaml.load(rf, Loader=yaml.FullLoader)
        info["validation_data"]["prompts"] = [condition_list[0]]
        info["validation_data"]["video_length"] = video_len
        info_updated = info
    with open("./condition.yaml", "w") as yf:
        yaml.dump(info_updated, yf, sort_keys=False)
    #save_name = input("Name of output folder: ")
    working_directory = "/workspace/animation_from_TP/FollowYourPose/"
    subprocess.run([f"TORCH_DISTRIBUTED_DEBUG=DETAIL accelerate launch txt2video.py --config=\"/workspace/animation_from_TP/condition.yaml\" --skeleton_path=\"{posepath}\" --file_name=\"animation\""], shell=True, cwd=working_directory)
    print("{} process is finished.".format(model))

def main():
    #parser = argparse.ArgumentParser(description="prompt of action and background")

    #args = parser.parse_args()

    assert os.path.exists("./condition_list.txt")
    with open("./condition_list.txt", 'r') as f:
        texts = f.readlines()
    condition_list = [t.replace("\n", "")for t in texts]
    print(condition_list)

    run_follow("FollowYourPose", condition_list)

if __name__ == "__main__":
    main()
