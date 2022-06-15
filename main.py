from random import shuffle

import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import glob
import re

xcoords = [x for x in range(1,500)]
arr = [x for x in range(1,500)]

shuffle(arr)

def natural_key(string_):
    """See https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def plot_frame(xcoords, arr, loopcount, folder):
    l = []
    # (arr[i]/len(arr))
    for i in range(0, len(arr)):
        l.append(((arr[i]/len(arr)),(arr[i]/len(arr)),0.5))
    plt.cla()
    plt.figure(facecolor='#2d7d78')
    plt.bar(xcoords, arr, width=1, color=l)
    plt.axis("off")
    plt.savefig(folder + "/frame" + str(loopcount) + ".jpg")


def render_video(video_name, image_folder):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images = sorted(images, key=natural_key)
    images = images + [images[-1] for x in range(20)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 30, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def insertion_sort(arr, folder):
	os.mkdir(folder + "/")
	for i in range(len(arr)-1):
		p = i
		while p > -1:
			if arr[p+1] < arr[p]:
				temp = arr[p]
				arr[p] = arr[p + 1]
				arr[p + 1] = temp
				p = p - 1
			else:
				break
		plot_frame(xcoords, arr, i, folder)
	return arr

def bubble_sort(arr, folder):
    os.mkdir(folder + "/")
    swapped = True;
    loopcount = 0
    while swapped:
        loopcount += 1
        swapped = False;
        for x in range(len(arr)-1):
            if arr[x] > arr[x+1]:
                arr[x],arr[x+1], swapped = arr[x+1], arr[x], True;
        plot_frame(xcoords, arr, loopcount, folder)
    return arr;

arrcopy = arr.copy()
insertion_sort(arr, "insertion_frames")
render_video("insertion.mp4", "insertion_frames")

# bubble_sort(arrcopy, "bubble_frames")
# render_video("bubble.mp4", "bubble_frames")