import csv
import json
import os
import re
import shutil

nameList = []
partList = []
fileName = ""
catList = dict()

if os.path.exists("../assets2"):
    shutil.rmtree("../assets2");
	
if os.path.exists("../json_set1"):
    shutil.rmtree("../json_set1")
	
if os.path.exists("../json_set2"):
    shutil.rmtree("../json_set2")
	
if os.path.exists("../output"):
    shutil.rmtree("../output")
	
os.mkdir("../assets2")
os.mkdir("../output")

with open("../assets/catalog_data.csv", "r", encoding="utf-8-sig") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if(row['PARTNUMBER'] != ''):
            partList.append(row['PARTNUMBER'])
        if(row['CATENTRY_ID'] != ''):
            catList.update({row['PARTNUMBER'] : row['CATENTRY_ID']})
        if(row['NAME'] != ''):
            nameList.append(row['NAME'])

pList = partList
partList = list(set(partList))

with open ("../assets/catalog_data.csv", "r", encoding = "utf-8-sig") as infile:
    for row in infile:
            if os.path.exists("../output/"+row.partition(",")[0]+".txt"):
                mode = 'a'
            else:
                mode = 'w'
            with open ("../output/"+row.partition(",")[0]+".txt", mode) as outfile:
                if (mode == 'w'):
                    outfile.write("PARTNUMBER,CATENTRY_ID,BRAND,CATEGORY,NAME,ATTRIBUTENAME,ATTRIBUTE,SHORTDESCRIPTION,LONGDESCRIPTION,OFFERPRICE")
                    outfile.write("\n")
                outfile.write(str(row))
with open ("../assets/2.txt", "r", encoding = "utf-8-sig") as infile:
    for row in infile:
        for i in range(len(nameList)):
            if nameList[i] in row:
                fileName = nameList[i]
        if os.path.exists("../assets2/"+fileName+".txt"):
            mode = 'a'
        else:
            mode = 'w'
        with open ("../assets2/"+fileName+".txt", mode) as outfile:
            outfile.write(str(row))

partNamePair = dict()
for i in range (len(partList)):
    try:
        with open ("../output/"+partList[i]+".txt", "r", encoding = "utf-8-sig") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                partNamePair.update({row['PARTNUMBER'] : row['NAME']})
    except OSError:
            pass
#partNamePairUnique = {}

#for key,value in partNamePair.items():
#    if value not in partNamePairUnique.values():
#        partNamePairUnique[key] = value

parentCatentryList = {}

for i in range (len(partList)):
    with open ("../output/"+partList[i]+".txt", "a") as outfile:
        try:
            #print(partNamePairUnique.get(partList[i], "duck"))
            with open ("../assets2/"+partNamePair.get(partList[i], "duck")+".txt", "r", encoding = "utf-8-sig") as infile:
                for row in infile:
                    parentCatentryList.update({partList[i] : row.partition(",")[0]})
                    row = row.replace(row.partition(",")[0], partList[i])
                    row = row.replace(row.split(",",2)[1], catList.get(partList[i]))
                    outfile.write(row)
        except OSError:
            pass

jsonNest = {}

for i in range (len(partList)):
    with open ("../output/"+partList[i]+".txt", "r", encoding = "utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        jsonNest = {}
        for row in reader:
            count = pList.count(partList[i])
            if jsonNest is not None:
                jsonNest[row['ATTRIBUTENAME']] = row['ATTRIBUTE']
                count = count-1
            if (count == 1):            
                del row['ATTRIBUTE']
                del row['ATTRIBUTENAME']
                #row['MRP'] = float(row['MRP'])
                row['OFFERPRICE'] = float(row['OFFERPRICE'])
                row['ATTRIBUTES'] = jsonNest
                row['PARENTPARTNUMBER'] = parentCatentryList.get(partList[i],"duck")
                if row['PARENTPARTNUMBER'] == "duck":
                    if len(row['PARTNUMBER'].rsplit("_", 1)[-1]) == 4:
                        row['PARENTPARTNUMBER'] = row['PARTNUMBER']
                    else:
                        row['PARENTPARTNUMBER'] = row['PARTNUMBER'][:-2]
                try:
                    os.makedirs("../json_set1/" + row['CATEGORY'])
                except OSError:
                    pass
                with open ("../json_set1/" + row['CATEGORY']+"/" + row['PARTNUMBER'] + ".json", "w") as outfile:
                    json.dump(row, outfile, sort_keys=True, indent=4, ensure_ascii=False)

jsonNest = {}

for i in range (len(partList)):
    with open ("../output/"+partList[i]+".txt", "r", encoding = "utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        jsonNest = {}
        strMod = []
        for row in reader:
            count = pList.count(partList[i])
            if jsonNest is not None:
                jsonNest[row['ATTRIBUTENAME']] = row['ATTRIBUTE']
                count = count-1
            if (count == 1):            
                del row['ATTRIBUTE']
                del row['ATTRIBUTENAME']
                #row['MRP'] = float(row['MRP'])
                row['OFFERPRICE'] = float(row['OFFERPRICE'])
                row['ATTRIBUTES'] = jsonNest
                row['PARENTPARTNUMBER'] = parentCatentryList.get(partList[i],"duck")
                jsonMod = jsonNest.copy()
                s = ""
                for k,v in jsonMod.items():
                    try:
                        if re.search('color', k, re.IGNORECASE):
                            jsonMod['color'] = jsonMod.pop(k)
                        if re.search('size', k, re.IGNORECASE):
                            jsonMod['size'] = jsonMod.pop(k)
                        if re.search('brand', k, re.IGNORECASE):
                            jsonMod['brand'] = jsonMod.pop(k)
                        if re.search('type', k, re.IGNORECASE):
                            jsonMod['type'] = jsonMod.pop(k)
                        if re.search('style', k, re.IGNORECASE):
                            jsonMod['style'] = jsonMod.pop(k)
                        if re.search('volts', k, re.IGNORECASE):
                            jsonMod['volts'] = jsonMod.pop(k)
                        if re.search('watts', k, re.IGNORECASE):
                            jsonMod['watts'] = jsonMod.pop(k)
                        if re.search('category', k, re.IGNORECASE):
                            jsonMod['category'] = jsonMod.pop(k)
                        if re.search('speed', k, re.IGNORECASE):
                            jsonMod['speed'] = jsonMod.pop(k)
                        k.replace("Kitchenware", "")
                    except KeyError:
                        pass
                stratt = ""
                for k,v in jsonMod.items():
                    stratt = v + " " + k
                    strMod.append(stratt)
                row['MODATTRIBUTES'] = str(set(strMod)).replace("{","").replace("}","")
                if row['PARENTPARTNUMBER'] == "duck":
                    if len(row['PARTNUMBER'].rsplit("_", 1)[-1]) == 4:
                        row['PARENTPARTNUMBER'] = row['PARTNUMBER']
                    else:
                        row['PARENTPARTNUMBER'] = row['PARTNUMBER'][:-2]
                try:
                    os.makedirs("../json_set2/" + row['CATEGORY'])
                except OSError:
                    pass
                with open ("../json_set2/" + row['CATEGORY']+"/" + row['PARTNUMBER'] + ".json", "w") as outfile:
                    json.dump(row, outfile, sort_keys=True, indent=4, ensure_ascii=False)
            
