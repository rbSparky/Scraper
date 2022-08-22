from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import jellyfish

#jellyfish.jaro_distance(u'jellyfish', u'smellyfish')

global link
global jsonDat
global allData
allData = 0
data = []


def table():
    
    global allData
    allData = 0

    html = urlopen(link)
    bsObj = BeautifulSoup(html)
    tot = ""

    #iterate through all find_alls
    #ask user which one they need
    for sibling in bsObj.find("table").tr.next_siblings:
         print(sibling)
         tot += str(sibling)
    f = open("out2.txt", "w")
    f.write(tot)
    f.close()


    f = open("out2.txt", "r")

    data = f.read()
    f.close()
    dat = data.split('</tr>')
    
    global jsonDat
    jsonDat = []
    
    for i in dat: 
        print(re.findall("\>(.*?)\<",i), '\n\n')
        jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))
    
    jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
    
    f = open("data2.json", "w")
    f.write(jsonString)
    f.close()
    
def lis():        
    global allData
    allData = 0

    html = urlopen(link)
    bsObj = BeautifulSoup(html)
    tot = ""
    
    for sibling in bsObj.find("ul").li.next_siblings:
         print(sibling)
         tot += str(sibling)
    f = open("out3.txt", "w")
    f.write(tot)
    f.close()

    f = open("out3.txt", "r")
    data = f.read()
    f.close()
    dat = data.split('</li>')

    global jsonDat
    jsonDat = []

    for i in dat: 
        print(re.findall("\>(.*?)\<",i), '\n\n')
        jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))
    
    jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
    
    f = open("dataList.json", "w")
    f.write(jsonString)
    f.close()

def exall():
    global allData
    allData = 1
    html = str(urlopen(link).read())
    print(html)
    global jsonDat
    jsonDat = []
    
    
    print(re.findall("\>(.*?)\<",html), '\n\n')
    jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",html))))

    jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
    
    f = open("dataAll.json", "w")
    f.write(jsonString)
    f.close()
    

def findSimilar():
    s = input('enter string to which similarity is to be calculated:')
    similarity = []

    global jsonDat
    global allData
    
    idx = 0
    for j in jsonDat:
        for i in j:
            if allData == 0:
                similarity.append([jellyfish.jaro_distance(i, s), i, j])
            else:
                similarity.append([jellyfish.jaro_distance(i, s), i, idx])
            if len(i) == 1:
                similarity[idx][0] -= 1
            idx += 1

    similarity.sort(reverse=True)
            

    print('top 10 similar lines')
    for i in range(0, 10):
        print(similarity[i], '\n')


pages = set()

def sitemap(wikilink):    
    global pages    
    global link
    html = urlopen(wikilink)
    bsObj = BeautifulSoup(html)
    for links in bsObj.findAll("a", href=re.compile('/')):
        if 'href' in links.attrs:
            try:
                if links.attrs['href'] not in pages:
                    #We have encountered a new page
                    newPage = links.attrs['href']
                    -
                    if link not in newPage:
                        print(newPage)
                        pages.add(newPage)
                        sitemap(link+newPage)
            except:
                print('error')


def menu():
    global link
    c = int(input('''
    1. Enter Link
    2. Extract tabular data
    3. Extract list data
    4. Extract all data
    5. Find similar
    6. Get sitemap
    :'''))
    if c==1:        
        link = input('\nenter link:')
    elif c==2:
        table()
    elif c==3:
        lis()
    elif c==4:
        exall()
    elif c==5:
        findSimilar()
    elif c==6:
        sitemap(link)
    else:
        return
    menu()

menu()
