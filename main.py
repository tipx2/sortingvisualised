from random import shuffle

import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np
import cv2
import os
import glob
import re


def natural_key(string_):
    """See https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def plot_frame(xcoords, arr, loopcount, folder, greenlines, frame_rate):
    
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
        else:
            l.append(((arr[i]/len(arr)),0,(arr[i]/len(arr))))

    plt.figure(facecolor='#e68332')
    plt.bar(xcoords, arr, width=1, color=l)
    plt.axis("off")
    plt.savefig(folder + "/frame" + str(loopcount) + ".jpg")
    plt.close()


def render_video(video_name, image_folder, frame_rate):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
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
    
    audio = mp.AudioFileClip(output)
    video1 = mp.VideoFileClip(video)
    final = video1.set_audio(audio)
    final.write_videofile(output + "_final.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')


def insertion_sort(arr, folder, frame_rate):
	os.mkdir(folder + "/")
	os.mkdir("sounds_" + folder + "/")
	loopcount = 0
	for i in range(len(arr)-1):
		p = i
		while p > -1:
			loopcount += 1
			plot_frame(xcoords, arr, loopcount, folder, [p, p + 1], frame_rate)
			if arr[p+1] < arr[p]:
				temp = arr[p]
				arr[p] = arr[p + 1]
				arr[p + 1] = temp
				p = p - 1
			else:
				break
	return sounds

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
                plot_frame(xcoords, arr, loopcount, folder, [x, x+1], frame_rate)
                arr_sorted = False
                break
            else:
                plot_frame(xcoords, arr, loopcount, folder, [], frame_rate)
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
            plot_frame(xcoords, arr, loopcount, folder, [x+1], frame_rate)
            if arr[x] > arr[x+1]:
                arr[x],arr[x+1], swapped = arr[x+1], arr[x], True
    loopcount += 1
    plot_frame(xcoords, arr, loopcount, folder, [], frame_rate)


xcoords = [x for x in range(1,50)]
arr = [x for x in range(1,50)]

shuffle(arr)

# insertion_sort(arr, "insertion_frames", 30)
# render_video("insertion.mp4", "insertion_frames", 30)
# render_audio("insertion.wav", "sounds_insertion_frames", "insertion.mp4")

bubble_sort(arr, "bubble_frames", 60)
render_video("bubble1.mp4", "bubble_frames", 60)
render_audio("bubble.wav", "sounds_bubble_frames", "bubble1.mp4")

# bogo_sort(arr, "bogo_frames", 60)
# render_video("bogo.mp4", "bogo_frames", 60)
# render_audio("bogo.wav", "sounds_bogo_frames", "bogo.mp4")