from random import shuffle

import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from pydub import AudioSegment
import numpy as np
import cv2
import os
import re


def natural_key(string_):
    """See https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def plot_frame(xcoords, arr, loopcount, folder, lines, frame_rate):
    greenlines = lines["greenlines"]
    redlines = lines["redlines"]
    
    if len(greenlines) == 0:
        sound = 0
    else:
        sound = arr[greenlines[0]]
        
    sps = 44100
    freq_hz = 440.0
    duration = (1/frame_rate)
    vol = 0.3

    esm = np.arange(duration * sps)
    wf = np.sin(sound * np.pi * esm * freq_hz / sps)
    wf_quiet = wf * vol
    wf_int = np.int16(wf_quiet * 32767)
    write("sounds_" + folder + "/sample" + str(loopcount) + ".wav", sps, wf_int)
    
    
    l = []
    # (arr[i]/len(arr))
    for i in range(0, len(arr)):
        if i in greenlines:
            l.append((0.1,1,0.1))
        elif i in redlines:
            l.append((1,0.1,0.1))
        else:
            l.append((0,0.5,(arr[i]/len(arr))))

    plt.figure(facecolor='#a5ffd6')
    plt.bar(xcoords, arr, width=1, color=l)
    plt.axis("off")
    plt.savefig(folder + "/frame" + str(loopcount) + ".png")
    plt.close()


def render_video(video_name, image_folder, frame_rate):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images = sorted(images, key=natural_key)
    images = images + [images[-1] for x in range(20)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, frame_rate, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def render_audio(output, folder, video):
    sounds = [snd for snd in os.listdir(folder) if snd.endswith(".wav")]
    sounds = sorted(sounds, key=natural_key)
    sounds = sounds + [sounds[-1] for x in range(20)]
    
    bigsound = AudioSegment.empty()
    for sound in sounds:
        bigsound += AudioSegment.from_wav(folder + "/" + sound)
    bigsound.export(output, format="wav")


def insertion_sort(arr, folder, frame_rate):
	os.mkdir(folder + "/")
	os.mkdir("sounds_" + folder + "/")
	loopcount = 0
	for i in range(len(arr)-1):
		p = i
		while p > -1:
			loopcount += 1
			plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[p, p + 1], "redlines":[]}, frame_rate)
			if arr[p+1] < arr[p]:
				temp = arr[p]
				arr[p] = arr[p + 1]
				arr[p + 1] = temp
				p = p - 1
			else:
				break

def bogo_sort(arr, folder, frame_rate):
    arr_sorted = False
    os.mkdir(folder + "/")
    os.mkdir("sounds_" + folder + "/")
    loopcount = 0
    while not arr_sorted:
        loopcount += 1
        shuffle(arr)
        for x in range(len(arr)-1):
            if arr[x] > arr[x+1]:
                plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[x, x+1], "redlines":[]}, frame_rate)
                arr_sorted = False
                break
            else:
                plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[], "redlines":[]}, frame_rate)
                arr_sorted = True



def bubble_sort(arr, folder, frame_rate):
    os.mkdir(folder + "/")
    os.mkdir("sounds_" + folder + "/")
    swapped = True
    loopcount = 0
    while swapped:
        swapped = False
        for x in range(len(arr)-1):
            loopcount += 1
            plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[x+1], "redlines":[]}, frame_rate)
            if arr[x] > arr[x+1]:
                arr[x],arr[x+1], swapped = arr[x+1], arr[x], True
    loopcount += 1
    plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[], "redlines":[]}, frame_rate)

def swapPositions(lis, pos1, pos2):
    lis[pos1], lis[pos2] = lis[pos2], lis[pos1]


def selection_sort(arr, folder, frame_rate):
    os.mkdir(folder + "/")
    os.mkdir("sounds_" + folder + "/")
    loopcount = 0
    for x in range(len(arr)-1):
        lowest = arr[x]
        for y in range(len(arr[x:])):
            loopcount += 1
            if arr[x:][y] < lowest:
                lowest = arr[x:][y]
            plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[arr.index(arr[x:][y]),x], "redlines":[arr.index(lowest)]}, frame_rate)
            
        
        lowest = min(arr[x:])
        swapPositions(arr, x, arr.index(lowest))
        
        
    plot_frame(xcoords, arr, loopcount, folder, {"greenlines":[], "redlines":[]}, frame_rate)

xcoords = [x for x in range(1,100)]
arr = [x for x in range(1,100)]

shuffle(arr)

# insertion_sort(arr, "insertion_frames", 30)
# render_video("insertion.mp4", "insertion_frames", 30)
# render_audio("insertion.wav", "sounds_insertion_frames", "insertion.mp4")

# bubble_sort(arr, "bubble_frames", 60)
# render_video("bubble1.mp4", "bubble_frames", 60)
# render_audio("bubble.wav", "sounds_bubble_frames", "bubble1.mp4")

# bogo_sort(arr, "bogo_frames", 15)
# render_video("bogo.mp4", "bogo_frames", 15)
# render_audio("bogo.wav", "sounds_bogo_frames", "bogo.mp4")

selection_sort(arr, "selection_frames", 30)
render_video("selection.mp4", "selection_frames", 30)
render_audio("selection.wav", "sounds_selection_frames", "selection.mp4")