import torch
from model import Model
from hf_utils import get_model_list
import argparse

model_list = get_model_list()
#model = Model(device = "cuda", dtype = torch.float16)

#for idx, name in enumerate(model_list):
#  print(idx, name)
#idx = int(input("Select the model by the listed number: ")) # select the model of your choice
#prompt = input("Prompt: ")
#out_path, fps = f"./text2video_{prompt.replace(' ','_')}.mp4", 4
#params = {"t0": 44, "t1": 47 , "motion_field_strength_x" : 12, "motion_field_strength_y" : 12, "video_length": 24}
#model.process_text2video(prompt, model_name = model_list[idx], fps = fps, path = out_path, **params)

model = Model(device = "cuda", dtype = torch.float16)

parser = argparse.ArgumentParser(description="prompt")
parser.add_argument('--text_file', default='', type=str, help='file name')
args = parser.parse_args()

texts = []
if args.text_file != '':
    with open(args.text_file, 'r') as f:
        texts = f.readlines()
    texts = [t.replace("\n", "") for t in texts]

prompt = texts[0]
print(prompt)
#prompt = input("Prompt: ")
params = {"t0": 44, "t1": 47 , "motion_field_strength_x" : 12, "motion_field_strength_y" : 12, "video_length": 8}

#out_path, fps = f"./text2video_{prompt.replace(' ','_')}.mp4", 4
out_path, fps = f"../animation_from_TP/static/animation/{prompt.replace(' ', '_')}.mp4", 4
model.process_text2video(prompt, fps = fps, path = out_path, **params)
