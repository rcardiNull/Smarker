"""
This file performs image segmentations
iterates oover directory and saves entries in the separate folder
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os



def thresholding(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # to greyscale
    ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY_INV)  # inverse binary <80 turn black
    return thresh


#  Preprocessing
def preprocessing():
    thresh_img = thresholding(img)
    # Dilation -> detect individual lines
    kernel = np.ones((3, 85), np.uint8)  # change the size according to image
    dilated = cv2.dilate(thresh_img, kernel, iterations=1)
    # Contours
    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # sort the contour lines
    sorted_contours_lines = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])  # contains (x,y,w,h)
    # Line Segmentation
    img2 = img.copy()  # make a copy of the original image
    plt.imshow(img2)
    for ctr in sorted_contours_lines:
        x, y, w, h = cv2.boundingRect(ctr)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (40, 100, 250), 2)
    return thresh_img,sorted_contours_lines,dilated


def textSegmentation():
    # Text Segmentation
    # finding contour of individual words in a sentence
    # dilation
    thresh_img,sorted_contours_lines,dilated=preprocessing()
    kernel = np.ones((3, 15), np.uint8)
    dilated2 = cv2.dilate(thresh_img, kernel, iterations=1)
    plt.imshow(dilated2, cmap='gray')
    
    plt.show()

    img3 = img.copy()
    words_list = []
    for line in sorted_contours_lines:
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
    for line in sorted_contours_lines:
        if cv2.contourArea(line) < 400:
            continue
        line_list.append([x+x2, y+y2, x+x2+w2, y+y2+h2])
        
    # effort to eliminate repeating entries. 
    # make a copy of original image
    img4 = img.copy()

    # iterate each contour
    for ctr in sorted_contours_lines:
        x,y,w,h = cv2.boundingRect(ctr)
        cv2.rectangle(img4,(x,y),(x+w,y+h),(40,100,500),2)
    plt.imshow(img4);

    from matplotlib.pyplot import imshow,show

    line_list = []
    for line in sorted_contours_lines:
        if cv2.contourArea(line)<400:
            continue
        x2,y2,w2,h2 = cv2.boundingRect(line)
        line_list.append([x+x2,y+y2,x+x2+w2,y+y2+h2])

    
    for n in range(len(line_list[:])):       
        for line in sorted_contours_lines:
            n_line = words_list[n] # run through n-th word in the list
            roi = img4[n_line[1]:n_line[3],n_line[0]:n_line[2]]        
        imshow(roi)
        show()
        entry = Image.fromarray(roi)
        entry_path = "/home/pi2/camCombo/Smarker/SimpleHTR/segOut" 
        entry.save(f"{entry_path}/entry_{d}_{n}.png")
        print(n)
      
        
# _______________MAINLOOP_______________

# Index the image directory and Segment every image in the directory
import os
sourceDirList=os.listdir("/home/pi2/camCombo/Smarker/SimpleHTR/LineSegmentation/sourceImg")
sourceDir=("/home/pi2/camCombo/Smarker/SimpleHTR/LineSegmentation/sourceImg/")
print("This folder contains {len_sourceDirList} files".format(len_sourceDirList=len(sourceDirList)))
d=0      
for imageEntry in sourceDirList:
    d=d+1
    print(imageEntry)
    print(f"Starting Segmentation on {imageEntry}")
    full_img_path=str(sourceDir+imageEntry)
    #print(full_img_path)
    img=cv2.imread(full_img_path)
    h, w, c = img.shape  # load dimensions
    if w > 1000:
        new_w = 1000
        ar = w/h # aspect ratio
        new_h = int(new_w/ar)
        img = cv2.resize(img,(new_w,new_h),interpolation=cv2.INTER_AREA)
    plt.imshow(img);
    textSegmentation()
