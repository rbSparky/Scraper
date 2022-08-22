import re 
import json

f = open("out3.txt", "r")
data = f.read()
f.close()
dat = data.split('</li>')

jsonDat = []

for i in dat: 
    print(re.findall("\>(.*?)\<",i), '\n\n')
    jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))

jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)

f = open("dataList.json", "w")
f.write(jsonString)
f.close()
