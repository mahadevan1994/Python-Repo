import csv
import json
import os
import shutil
import time

start_time = time.time()
feedFile1Map = dict()
feedFile2Map = dict()
deltaList = []

with open("FeedFiles/old.csv", "r", encoding="utf-8-sig") as infile:
    reader = csv.DictReader(infile)
    headers = reader.fieldnames
    for row in reader:
        feedFile1Map.update({row['ScoreEmailid'] : row['FPEmailId']+","+row['SubStartdate']+","+row['SubEndDate']+","+row['Status']+","+row['MarketingConsent']+","+row['ScoreEmailid']+"\n"})

with open("FeedFiles/new.csv", "r", encoding="utf-8-sig") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        feedFile2Map.update({row['ScoreEmailid'] : row['FPEmailId']+","+row['SubStartdate']+","+row['SubEndDate']+","+row['Status']+","+row['MarketingConsent']+","+row['ScoreEmailid']+"\n"})

feedFile2Keys = feedFile2Map.keys()

i=0

for item in feedFile2Keys:
    if item in feedFile1Map:
        if feedFile1Map.get(item) != feedFile2Map.get(item):
            deltaList.append(feedFile2Map.get(item))
            i=i+1
    else:
        deltaList.append(feedFile2Map.get(item))
        i=i+1

deltaFileContent = ""
deltaFileContent = deltaFileContent + (','.join(headers))+"\n"
for res in deltaList:
    deltaFileContent = deltaFileContent + res
deltaFileContent = deltaFileContent.rstrip('\n')

try:
    os.makedirs("Delta")
except OSError:
    pass

try:
    with open ("Delta/deltaFile.csv", "w+") as outfile:
        outfile.write(deltaFileContent)

    print(str (i)+" records modified, delta file created successfully. Check Delta/deltaFile.csv")
    print("\n--- %s seconds ---" % (time.time() - start_time))

except Exception as e: print(e)                  
