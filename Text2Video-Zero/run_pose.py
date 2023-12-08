import torch
import argparse
from model import Model

model = Model(device = "cuda", dtype = torch.float16)

parser = argparse.ArgumentParser(description="prompt and video")
parser.add_argument('--text_file', default='', type=str, help='file path')
#parser.add_argument('--video_path', default='/workspace/animation_from_TP/static/pose_video/skel/skel_00.mp4', type=str, help='file path')
parser.add_argument('--video_path', default='/workspace/animation_from_TP/static/pose_video/waiving.mp4', type=str, help='file path')
args = parser.parse_args()

texts = []
if args.text_file != '':
    with open(args.text_file, 'r') as f:
        texts = f.readlines()
    texts = [t.replace("\n", "") for t in texts]

#motion_path = '/workspace/animation_from_TP/static/pose_video/skel/skel_00.mp4'
#motion_path = './Unknown_AdobeExpress.mp4'
prompt = texts[0]
motion_path = args.video_path
out_path = f"../animation_from_TP/animation.mp4"
model.process_controlnet_pose(motion_path, prompt=prompt, save_path=out_path)
