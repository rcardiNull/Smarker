
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


img = cv2.imread('/home/thehost/Smarker/SimpleHTR/LineSegmentation/sourceImg/NewPhoto.png')  # input image file.
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h, w, c = img.shape  # load dimensions

# resize the image
if w > 1000:
    new_w = 1000
    ar = w/h  # aspect ratio
    new_h = int(new_w/ar)  # new height
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)


def thresholding(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # to greyscale
    ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY_INV)  # inverse binary <80 turn black
    return thresh


#  Preprocessing

thresh_img = thresholding(img)
# Dilation -> detect individual lines
kernel = np.ones((3, 85), np.uint8)  # change the size according to image
dilated = cv2.dilate(thresh_img, kernel, iterations=1)
# Contours
(contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# sort the contour lines
sorted_contour_lines = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])  # contains (x,y,w,h)


# Line Segmentation
img2 = img.copy()  # make a copy of the original image

for ctr in sorted_contour_lines:
    x, y, w, h = cv2.boundingRect(ctr)
    cv2.rectangle(img2, (x, y), (x+w, y+h), (40, 100, 250), 2)



# Text Segmentation
# finding contour of individual words in a sentence
# dilation
kernel = np.ones((3, 15), np.uint8)
dilated2 = cv2.dilate(thresh_img, kernel, iterations=1)
# plt.imshow(dilated2, cmap='gray')

img3 = img.copy()
words_list = []
for line in sorted_contour_lines:
    # roi of each line
    x, y, w, h = cv2.boundingRect(line)
    roi_line = dilated[y:y + w, x:x + w]  # dilated2 for letter segm or word in a line

    # draw contours on each word
    (cnt, hierarchy) = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contour_words = sorted(cnt, key=lambda cntr: cv2.boundingRect(cntr)[0])

    for word in sorted_contour_words:
        if cv2.contourArea(word) < 400:
            continue

        x2, y2, w2, h2 = cv2.boundingRect(word)
        words_list.append([x + x2, y + y2, x + x2 + w2, y + y2 + h2])
        cv2.rectangle(img3, (x + x2, y + y2), (x + x2 + w2, y + y2 + h2), (255, 255, 100), 2)

line_list = []
for line in sorted_contour_lines:
    if cv2.contourArea(line) < 400:
        continue
    line_list.append([x+x2, y+y2, x+x2+w2, y+y2+h2])

# effort to eliminate repeating entries.
# make a copy of original image
img4 = img.copy()
n = 0
images_path = "/home/thehost/Smarker/SimpleHTR/segOut"
for n in range(len(line_list[:])):
    n += 1
    for line in sorted_contour_lines:
        n_line = words_list[n]  # run through n-th word in the list
        roi = img4[n_line[1]:n_line[3], n_line[0]:n_line[2]]
    entry = Image.fromarray(roi)

    entry.save(f"{images_path}/entry_{n}.png")
