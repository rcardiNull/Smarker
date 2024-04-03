# THis file will preprocess data to be output for googleDoc

from spellchecker import SpellChecker
from datetime import date
import time
import re

print("Starting processing of received words")
entries = []
with open('/home/pi2/camCombo/Smarker/SimpleHTR/SimpleHTR/src/outputList.txt','r') as file:
    data = file.read()
    print("reading the input file")
    data = data.split('\n') #-> it is now a list

for entry in data: # for every entry in data 
    if entry.startswith(' * '):
        entries.append(entry)
        Sentries = "".join(entries)
res = re.findall(r"\[(.*?)\]",Sentries) # entry into a list 

print("check if in the list")
words = []
for i in res:
    if i not in words:
        words.append(i)
    else: continue

print("Appending to the file")
# Appending to a file
f = open('/home/pi2/camCombo/Smarker/SimpleHTR/SimpleHTR/src/fridgeList.txt','a')
f.write('˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚˚')
today = str(date.today())
f.write('\n')
f.write(today)
f.write('\n')
for wordy in words:    
    f.write(wordy)
    f.write('\n')
f.write('\n')
