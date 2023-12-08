#@title Create OpenPose style image sequence from motion data
from scipy.spatial.transform import Rotation
camera_pose = "(0.0,0,0,0,-1.5,-3.5)" #@param {type:"string"}
fov = 300 #@param {type:"number"}
import numpy as np
import torch
import cv2
from utils.motion_process import recover_from_ric
import tqdm
import ast
import os


OpenPoseIDs_to_SMPL = {
    "head": [15,(155,11,53)],
    "neck": [[13,(207,76,6)],[14,(207,76,6)]],
    "lshoulder": [16,(200,100,4)],
    "rshoulder": [17,(100,200,2)],
    "lelbow": [18,(200,200,0)],
    "relbow": [19,(6,200,1)],
    "lwrist": [20,(250,250,0)],
    "rwrist": [21,(0,250,0)],
    "lhip": [1,(5,160,103)],
    "rhip": [2,(0,50,150)],
    "lknee": [4,(0,200,200)],
    "rknee": [5,(4,4,200)],
    "lankle": [7,(0,255,255)],
    "rankle": [8,(0,1,250)],
    "leye": [0,(200,1,0)],
    "reye": [0,(200,1,0)],
    "lear": [0,(200,1,0)],
    "rear": [0,(200,1,0)],
    }

OpenPoseLimbs = [
    ["head","neck", (0,0,155)],
    ["neck","lshoulder", (150,50,3)],
    ["neck","rshoulder", (100,150,2)],
    ["lshoulder","lelbow", (150,150,0)],
    ["rshoulder","relbow", (100,200,1)],
    ["lelbow","lwrist", (200,200,0)],
    ["relbow","rwrist", (50,200,0)],
    ["neck","lhip", (1,158,3)],
    ["neck","rhip", (1,100,155)],
    ["lhip","lknee", (0,154,54)],
    ["rhip","rknee", (1,70,200)],
    ["lknee","lankle", (0,200,200)],
    ["rknee","rankle", (0,50,200)],
    ["head","leye", (200,0,200)],
    ["head","reye", (200,0,0)],
    ["lear","leye", (200,0,200)],
    ["rear","reye", (200,0,0)],
]

#from openpose, but rendered with an alpha value?
limb_colors = [[255, 0, 0],
               [255, 85, 0],
               [255, 170, 0],
               [255, 255, 0],
               [170, 255, 0],
               [85, 255, 0],
               [0, 255, 0],
              [0, 255, 85],
               [0, 255, 170],
               [0, 255, 255],
               [0, 170, 255],
               [0, 85, 255],
               [0, 0, 255],
               [85, 0, 255],
                [170, 0, 255],
               [255, 0, 255],
               [255, 0, 170],
               [255, 0, 85],
               [0, 0, 0]]


fx,fy = (fov,fov)
size = (512,512,3)
K = np.array([[fx, 0, size[0]/2],
              [0, fy, size[1]/2],
              [0, 0, 1]], dtype=np.float32)
D = np.zeros((5,1), dtype=np.float32)

pose_tuple = ast.literal_eval(camera_pose)

rvec = np.array(pose_tuple[0:3], dtype=np.float32)
tvec = np.array(pose_tuple[3:6], dtype=np.float32)

IMG_DIR = os.path.join(out_path, "images")
if not os.path.exists(IMG_DIR):
  os.mkdir(IMG_DIR)
else:
  !rm {os.path.join(IMG_DIR)}/*.jpg

with open(os.path.join(out_path,'motion.npy'), 'rb') as f:
  data = np.load(f)
  joints_num = 22
  joint = recover_from_ric(torch.from_numpy(data).float(), joints_num).numpy()

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  video = cv2.VideoWriter(f"{out_path}/skeleton.mp4", fourcc, 30,size[:2])
  for i,frame in enumerate(joint):
    img = np.zeros(size, dtype=np.uint8)
    scaler = 150
    offset = size[0]/2

    #original SMPL points
    # for k,j in enumerate(frame):
    #   cv2.circle(img, (int(j[0]*scaler+offset),int(-j[1]*scaler+offset)), 3, SMPL_joint_colors[k],-1)

    op_joints = {}
    op_joints3D = {}
    joint_size = 5
    limb_size = 3

    #compute joints from SMPL skeleton
    for k in OpenPoseIDs_to_SMPL:
      if k == "neck":
        a,b = OpenPoseIDs_to_SMPL[k]
        idx1,color = a
        idx2,c2 = b
        op_joints3D[k] = (np.array([frame[idx1]]) + np.array(frame[idx2]))/2
      else:
        idx, color = OpenPoseIDs_to_SMPL[k]
        op_joints3D[k] = np.array([frame[idx]])

    # construct eye and ear joints using shoulders and neck to head
    shoulder_vec = op_joints3D["lshoulder"] - op_joints3D["rshoulder"]
    shoulder_mag = np.linalg.norm(shoulder_vec)
    shoulder_vec /= shoulder_mag
    eye_mag = shoulder_mag/8
    head_neck_vec = op_joints3D["head"] - op_joints3D["neck"]
    head_neck_vec /= np.linalg.norm(head_neck_vec)
    forward_vec = np.cross(shoulder_vec, head_neck_vec)
    forward_vec /= np.linalg.norm(forward_vec)
    #eyes are slightly up and to the side
    op_joints3D["leye"] = op_joints3D["head"] + shoulder_vec*eye_mag + head_neck_vec*eye_mag
    op_joints3D["reye"] = op_joints3D["head"] - shoulder_vec*eye_mag + head_neck_vec*eye_mag
    #ears are toward the back of the head
    op_joints3D["lear"] = op_joints3D["head"] + shoulder_vec*eye_mag*2 - forward_vec*eye_mag*2 + head_neck_vec*eye_mag
    op_joints3D["rear"] = op_joints3D["head"] - shoulder_vec*eye_mag*2 - forward_vec*eye_mag*2 + head_neck_vec*eye_mag

    #push the head point forward to become the nose
    op_joints3D["head"] += forward_vec*eye_mag

    # transforms 3D points and check if back is facing camers
    r = Rotation.from_euler("xyz",rvec)
    zeros = np.zeros((1,3))
    for k in op_joints3D:
        op_joints3D[k] = r.apply(op_joints3D[k]) + tvec
        p = cv2.projectPoints(op_joints3D[k],zeros, zeros, K, D)[0][0][0]
        op_joints[k] = (int(p[0]),int(p[1]))
    camera_dir = -op_joints3D['neck']
    camera_dir /= np.linalg.norm(camera_dir)


    #check if back is toward camera
    shoulder_vec = op_joints3D["lshoulder"] - op_joints3D["rshoulder"]
    shoulder_mag = np.linalg.norm(shoulder_vec)
    shoulder_vec /= shoulder_mag
    eye_mag = shoulder_mag/8
    head_neck_vec = op_joints3D["head"] - op_joints3D["neck"]
    head_neck_vec /= np.linalg.norm(head_neck_vec)
    forward_vec = np.cross(shoulder_vec, head_neck_vec)
    forward_vec /= np.linalg.norm(forward_vec)

    camera_dot = np.dot(camera_dir, forward_vec.transpose())
    back_to_camera = camera_dot < -0.1

    #draw limbs
    for l in OpenPoseLimbs:
      color = tuple(reversed(l[2]))
      if back_to_camera:
        if l[0] in ["leye", "lear", "reye", "rear"]:
          continue
        if l[1] in ["leye", "lear", "reye", "rear"]:
          continue
      cv2.line(img, op_joints[l[0]],op_joints[l[1]], color,limb_size)

    #draw joints
    for k in OpenPoseIDs_to_SMPL:
      if k == "neck":
        a,b = OpenPoseIDs_to_SMPL[k]
        idx1,color = a
      else:
        idx, color = OpenPoseIDs_to_SMPL[k]
      if back_to_camera:
        if k in ["leye", "lear", "reye", "rear"]:
          continue
      color = tuple(reversed(color))
      cv2.circle(img, op_joints[k], joint_size, color,-1)

    #save video files
    cv2.imwrite(f"{IMG_DIR}/{i:03}.jpg", img)
    video.write(img)
video.release()

import mediapy as media
video2 = media.read_video(f"{out_path}/skeleton.mp4")
media.show_video(video2, fps=30, codec='gif')

