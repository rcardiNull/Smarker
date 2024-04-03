#!/usr/bin/env bash


# This script will automatically transfer every image in Photos
#folder to RPi3 server via SSH.
# and delete transferred image from the source

ssh thehost@thehost #make sure to add public/private keys

PHOTOS="/home/thehost/Desktop/cameraFiles/piPhotos/*"
for FILE in $PHOTOS
do 
    scp $FILE thehost@thehost:/home/thehost/Smarker/SimpleHTR/LineSegmentation/sourceImg/
    echo "File :  $FILE transferred"
    rm $FILE
    echo "File : $FILE deleted"
done

exit
