
#! /bin/bash

# Run the segmentation first
python ./LineSegmentation/Segmentation.py

# mount googleDrive
echo  "mounting Google Drive"
rclone mount gdrive: /home/pi2/mnt/gdrive --daemon
sleep 7

# Process all segmented images into words with main.py
search_dir=/home/pi2/camCombo/Smarker/SimpleHTR/segOut
echo "------------Loading Files------------"
n=1
cd ./SimpleHTR/src

for entry in $search_dir/*
do
  item=$entry
  echo "------------Testing File: $n  ------------------- "
  echo ">>>>___Working on $item ___<<<<"
  python main.py --img_file $item
  n=$((n+1))

done

# Preprocess output.txt to sorted fridgeList.txt
echo "Preprocessing output.txt to fridgeList.txt"
python3 /home/pi2/camCombo/Smarker/SimpleHTR/preProcess.py

# Remove all files from segOut folder
echo "Removing Segmented images fromt the segOut directory"
rm /home/pi2/camCombo/Smarker/SimpleHTR/segOut/*

# Move processed list into mounted googleDrive
echo " Appending results list into gDrive fridgeList.docx"
cat  /home/pi2/camCombo/Smarker/SimpleHTR/SimpleHTR/src/fridgeList.txt >> /home/pi2/camCombo/Smarker/SimpleHTR/fridgeList.docx
cp /home/pi2/camCombo/Smarker/SimpleHTR/fridgeList.docx  $HOME/mnt/gdrive/fridgeList.docx
# Removing entries from fridgeList.txt && output.txt
echo "Clearning up the Lists"
> /home/pi2/camCombo/Smarker/SimpleHTR/SimpleHTR/src/fridgeList.txt
> /home/pi2/camCombo/Smarker/SimpleHTR/SimpleHTR/src/outputList.txt
# unmount gdrive
echo " Unmounting the Google Drive"
umount /home/pi2/mnt/gdrive
