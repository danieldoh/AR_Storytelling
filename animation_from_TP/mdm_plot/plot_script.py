import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegFileWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.axes3d as p3
# import cv2
from textwrap import wrap

def list_cut_average(ll, intervals):
    if intervals == 1:
        return ll

    bins = math.ceil(len(ll) * 1.0 / intervals)
    ll_new = []
    for i in range(bins):
        l_low = intervals * i
        l_high = l_low + intervals
        l_high = l_high if l_high < len(ll) else len(ll)
        ll_new.append(np.mean(ll[l_low:l_high]))
    return ll_new


def plot_3d_motion(save_path, kinematic_tree, joints, title, dataset, figsize=(6.5, 6.5), fps=120, radius=3,
                   vis_mode='default', gt_frames=[]):
    matplotlib.use('Agg')

    #title = '\n'.join(wrap(title, 20))

    def init():
        ax.set_xlim3d([-radius / 2, radius / 2])
        ax.set_ylim3d([0, radius])
        ax.set_zlim3d([-radius / 3., radius * 2 / 3.])
        ax.grid(b=False)

    data = joints.copy().reshape(len(joints), -1, 3)

    # preparation related to specific datasets
    if dataset == 'kit':
        data *= 0.003  # scale for visualization
    elif dataset == 'humanml':
        data *= 1.3  # scale for visualization
    elif dataset in ['humanact12', 'uestc']:
        data *= -1.5 # reverse axes, scale for visualization

    fig = plt.figure(figsize=figsize, dpi=200)
    plt.tight_layout()
    plt.style.use("dark_background")
    ax = p3.Axes3D(fig)
    init()
    MINS = data.min(axis=0).min(axis=0)
    MAXS = data.max(axis=0).max(axis=0)
    #line = np.linspace(MINS, MAXS, len(data))
    colors_blue = ["#4D84AA", "#5B9965", "#61CEB9", "#34C1E2", "#80B79A"]  # GT color
    colors_orange = ["#DD5A37", "#D69E00", "#B75A39", "#FF6D00", "#DDB50E"]  # Generation color
    colors_mmpose = ["#0089FF", "#00DD01", "#FFA72E", "#0089FF", "#00DD01"]
    colors_openpose = ["#990000", "#993300", "#996600", "#999900", "#669900", "#339900", "#009900", "#009933", "#009966", "#009999", "#006699", "#003399", "#000099", "#330099", "#660099", "#990099", "#990066"]
    #colors = colors_openpose
    colors = colors_mmpose
    if vis_mode == 'upper_body':  # lower body taken fixed to input motion
        colors[0] = colors_blue[0]
        colors[1] = colors_blue[1]
    elif vis_mode == 'gt':
        colors = colors_blue

    frame_number = data.shape[0]

    height_offset = MINS[1]
    data[:, :, 1] -= height_offset
    trajec = data[:, 0, [0, 2]]

    data[..., 0] -= data[:, 0:1, 0]
    data[..., 2] -= data[:, 0:1, 2]

    #print("min: ", data.min(axis=0).min(axis=0))
    #print("max: ", data.max(axis=0).max(axis=0))
    #print(data)
    #line = np.linspace(data.min(axis=0).min(axis=0), data.max(axis=0).max(axis=0), 240)

    def update(index):
        ax.lines = []
        ax.collections = []
        ax.view_init(elev=120, azim=-90)
        ax.dist = 7.5

        used_colors = colors_blue if index in gt_frames else colors
        for i, (chain, color) in enumerate(zip(kinematic_tree, used_colors)):
            if i < 5:
                linewidth = 4.0
            else:
                linewidth = 2.0

            # midpoint of shoulder
            #data[index, [9], :] = (data[index, [16], :] + data[index, [17], :]) / 2

            ## assign variables
            #lshoulder = data[index, [16], :]
            #rshoulder = data[index, [17], :]
            #head = data[index, [15], :]
            #neck = data[index, [12], :]

            ## eye and ear

            #shoulder_vec = lshoulder - rshoulder
            #shoulder_mag = np.linalg.norm(shoulder_vec)
            #shoulder_vec /= shoulder_mag
            #eye_mag = shoulder_mag/8
            #head_neck_vec = head - neck
            #head_neck_vec /= np.linalg.norm(head_neck_vec)
            #forward_vec = np.cross(shoulder_vec, head_neck_vec)

            ##left eye
            #data[index, [10], :] = head + shoulder_vec*eye_mag + head_neck_vec*eye_mag
            ##right eye
            #data[index, [11], :] = head - shoulder_vec*eye_mag + head_neck_vec*eye_mag

            ##left eye
            #data[index, [3], :] = head + shoulder_vec*eye_mag*2 - forward_vec*eye_mag*2 + head_neck_vec*eye_mag
            ##right eye
            #data[index, [6], :] = head - shoulder_vec*eye_mag*2 - forward_vec*eye_mag*2 + head_neck_vec*eye_mag


            ax.plot3D(data[index, chain, 0], data[index, chain, 1], data[index, chain, 2], linewidth=linewidth, color=color)
            #ax.plot(data[index, chain, 0], data[index, chain, 1], linewidth=linewidth,
                      #color=color)

        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

    ani = FuncAnimation(fig, update, frames=frame_number, interval=1000 / fps, repeat=False)

    # writer = FFMpegFileWriter(fps=fps)
    ani.save(save_path, fps=fps)
    # ani = FuncAnimation(fig, update, frames=frame_number, interval=1000 / fps, repeat=False, init_func=init)
    # ani.save(save_path, writer='pillow', fps=1000 / fps)
    plt.close()
