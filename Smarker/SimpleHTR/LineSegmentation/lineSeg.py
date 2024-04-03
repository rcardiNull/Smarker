"""
This file is responsible for line segmentation of a provided image

We will break down the list of words into lines and then if necessary
perform word segmentation as well.

RETURN: file returns few individual images that have been recognized
as words/entries.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.pyplot import imshow, show



img = cv2.imread('testList.png')  # input image file.
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

h, w, c = img.shape  # load dimensions

# resize the image
if w > 1000:
    new_w = 1000
    ar = w/h # aspect ratio
    new_h = int(new_w/ar) # new height
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
# plt.imshow(img); # shows the resized image

# function to show thresholds of an image
# convert image to greyscale
# <80 turn the pixel to black

def thresholding(image):
    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # to greyscale
    ret,thresh =cv2.threshold(img_gray,80,255,cv2.THRESH_BINARY_INV) #inverse binary <80 turn balck
    # plt.imshow(thresh, cmap='gray') # display
    return thresh

thresh_img = thresholding(img)

# Dilation -> detect individual lines
kernel = np.ones((3, 85), np.uint8) # change the size according to image
dilated = cv2.dilate(thresh_img, kernel, iterations=1)
# plt.imshow(dilated, cmap='gray')

# Contours
(contours,heirarchy) = cv2.findContours(dilated.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
# sort the contour lines
sorted_contours_lines = sorted(contours, key=lambda ctr:cv2.boundingRect(ctr)[1])  #containg (x,y,w,h)

img2 = img.copy() # make a copy of the original image
words_list =[]
for ctr in sorted_contours_lines:
    x, y, w, h = cv2.boundingRect(ctr)
    cv2.rectangle(img2, (x,y), (x+w, y+h),(40,100,250), 2)
plt.imshow(img2)

# findign contour of individual words in a sentence
# dilation
kernel = np.ones((3,15), np.uint8)
dilated2 = cv2.dilate(thresh_img, kernel, iterations=1)
plt.imshow(dilated2, cmap='gray')

img3 = img.copy()
words_list = []
for line in sorted_contours_lines:
    # roi of each line
    x, y, w, h = cv2.boundingRect(line)
    roi_line = dilated[y:y + w, x:x + w]  # dilated2 for letter segm or word in a line

    # draw contours on each word
    (cnt, heirarchy) = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_countour_words = sorted(cnt, key=lambda cntr: cv2.boundingRect(cntr)[0])

    for word in sorted_countour_words:
        if cv2.contourArea(word) < 400:
            continue

        x2, y2, w2, h2 = cv2.boundingRect(word)
        words_list.append([x + x2, y + y2, x + x2 + w2, y + y2 + h2])
        cv2.rectangle(img3, (x + x2, y + y2), (x + x2 + w2, y + y2 + h2), (255, 255, 100), 2)

plt.imshow(img3)


line_list = []
for line in sorted_contours_lines:
    if cv2.contourArea(line) < 400:
        continue
    line_list.append([x+x2,y+y2,x+x2+w2,y+y2+h2])

# effort to eliminate repeating entries.
# make a copy of original image
img4 = img.copy()

# iterate each contour
for ctr in sorted_contours_lines:
    x,y,w,h = cv2.boundingRect(ctr)
    cv2.rectangle(img4,(x,y),(x+w,y+h),(40,100,250),2)
#plt.imshow(img4)

from matplotlib.pyplot import imshow,show

line_list = []
for line in sorted_contours_lines:
    if cv2.contourArea(line)<400:
        continue
    #x2,y2,w2,h2 = cv2.boundingRect(line)
    line_list.append([x+x2,y+y2,x+x2+w2,y+y2+h2])

n=0
for n in range(len(line_list[:])):
    n=n+1
    for line in sorted_contours_lines:
        n_line = words_list[n] # run through n-th word in the list
        roi = img4[n_line[1]:n_line[3],n_line[0]:n_line[2]]
    imshow(roi)
    show()
    entry = Image.fromarray(roi)
    entry.save(f"entry_{n}.png")
    #print(n)
