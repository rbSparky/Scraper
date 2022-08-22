import re
import json

f = open("out2.txt", "r")
data = f.read()
f.close()
dat = data.split('</tr>')

jsonDat = []

for i in dat: 
    #print(re.findall("\>(.*?)\<",i), '\n\n')
    jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))

for i in jsonDat:
    print(i)

jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)

f = open("data2.json", "w")
f.write(jsonString)
f.close()
