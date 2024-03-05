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
        width  = np.sqrt((c[1]-c[4])**2 + (c[2]-c[5])**2)
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


def normal():
    
    while True:
        file = input("Enter file path(*.csv): ")
        if file:
            break
    
    while True:
        stim = int(input("Enter last frame before stimulus: "))
        if stim:
            break
    
    temp = input("Enter frames to analyse (default: 900=30*30): ")
    frames = 0
    if not temp:
        frames = 900
    else:
        frames = int(temp)
    
    with open(file, 'r') as f:
        next(f)
        next(f)
        next(f)
        df = np.loadtxt(f, delimiter=',')
        print(df.shape)
        before = df[(stim-frames):stim, :]
        after  = df[(stim+1):(stim+frames+1), :]
        eye_opening_before  = create_eye_opening(before)
        eye_opening_after   = create_eye_opening(after)
        ear_position_before = create_ear_position(before)
        ear_position_after  = create_ear_position(after)
    
        eye_opening  = np.hstack([eye_opening_before, eye_opening_after])
        ear_position = np.hstack([ear_position_before, ear_position_after])
        
        print(eye_opening.shape)
        
        befores = np.array(['Before'] * 900)
        afters = np.array(['After'] * 900)
        
        timings = np.hstack([befores, afters])
        
        print(timings.shape)
        
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
    

def compare():
    file1 = input("Enter file path(*.csv) (1): ")
    file2 = input("Enter file path(*.csv) (2): ")
    stim1 = int(input("Enter last frame before stimulus (1): "))
    stim2 = int(input("Enter last frame before stimulus (2): "))

    

def main(mode):
    if mode == 'normal':
        normal()
    elif mode == 'compare':
        compare()
        
if __name__ == '__main__':
    main(sys.argv[1])