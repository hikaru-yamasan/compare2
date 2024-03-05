import sys
import numpy as np
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_eye_opening(matrix):
    eo = []
    for c in matrix:
        height = np.sqrt((c[7]-c[10])**2 + (c[8]-c[11])**2)
        width = np.sqrt((c[1]-c[4])**2 + (c[2]-c[5])**2)
        eo.append(height / width)
    return np.array(eo)


def create_ear_position(matrix):
    ep = []
    for c in matrix:
        temp_a = [c[1]-c[13], c[2]-c[14]]
        temp_b = [c[16]-c[13], c[17]-c[14]]
        theta = cal_deg(temp_a, temp_b)
        ep.append(theta)
    return np.array(ep)


def cal_deg(a, b):
    temp_dot = np.array(a) @ np.array(b)
    temp_norm = np.linalg.norm(a) * np.linalg.norm(b)
    temp_cos = temp_dot / temp_norm
    return np.degrees(np.arccos(temp_cos))


def normal(filepath: str, stim: int, frames: int):

    print('from pyshell: func `normal` called')

    try:
        f = open(filepath, 'r')
    except Exception as e:
        print('from pyshell')
        print(e)
    else:
        print('from pyshell: file opened')

    next(f)
    next(f)
    next(f)
    df = np.loadtxt(f, delimiter=',')
    before = df[(stim-frames):stim, :]
    after = df[(stim+1):(stim+frames+1), :]
    eye_opening_before = create_eye_opening(before)
    eye_opening_after = create_eye_opening(after)
    ear_position_before = create_ear_position(before)
    ear_position_after = create_ear_position(after)

    eye_opening = np.hstack([eye_opening_before, eye_opening_after])
    ear_position = np.hstack([ear_position_before, ear_position_after])

    befores = np.array(['Before'] * 900)
    afters = np.array(['After'] * 900)

    timings = np.hstack([befores, afters])

    eo = pd.DataFrame()
    eo['Timing'] = timings
    eo['EyeOpening'] = eye_opening

    ep = pd.DataFrame()
    ep['Timing'] = timings
    ep['EarPosition'] = ear_position

    fig = plt.figure()

    ax1 = fig.add_subplot(1, 2, 1)
    sns.boxplot(
        ax=ax1,
        data=eo,
        x='Timing',
        y='EyeOpening',
        palette='Pastel1',
    )

    ax2 = fig.add_subplot(1, 2, 2)
    sns.boxplot(
        ax=ax2,
        data=ep,
        x='Timing',
        y='EarPosition',
        palette='Pastel2',
    )
    plt.legend()
    plt.tight_layout()
    plt.show()

    f.close()

    return '[LOG] pyshell done!'


file = sys.stdin.readline().replace('\n', '')
stim = int(sys.stdin.readline())
frames = int(sys.stdin.readline())

print('from pyshell')
print(file)
print(stim)
print(frames)

normal(filepath=file, stim=stim, frames=frames)
