from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import jellyfish


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
    try:
      for sibling in bsObj.find("table").tr.next_siblings:
           #(sibling)
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
          #(re.findall("\>(.*?)\<",i), '\n\n')
          jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))
      
      jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
      
      f = open("data2.json", "w")
      f.write(jsonString)
      f.close()
      return jsonString
    except:
      return ''
    
def lis():        
    global allData
    allData = 0

    html = urlopen(link)
    bsObj = BeautifulSoup(html)
    tot = ""

    try:
      for sibling in bsObj.find("ul").li.next_siblings:
           #(sibling)
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
          #(re.findall("\>(.*?)\<",i), '\n\n')
          jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",i))))
      
      jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
      
      f = open("dataList.json", "w")
      f.write(jsonString)
      f.close()
      return jsonString
    except:
      return ''
    

def exall():
    global allData
    allData = 1
    html = str(urlopen(link).read())
    #(html)
    global jsonDat
    jsonDat = []
    
    
    #(re.findall("\>(.*?)\<",html), '\n\n')
    jsonDat.append(list(filter(None, re.findall("\>(.*?)\<",html))))

    jsonString = json.dumps(jsonDat, indent=4, sort_keys=True)
    
    f = open("dataAll.json", "w")
    f.write(jsonString)
    f.close()  
    return jsonString
    
    

def findSimilar(s):
    #s = input('enter string to which similarity is to be calculated:')
    similarity = []

    global jsonDat
    global allData
    
    idx = 0
    for j in jsonDat:
        for i in j:
            if allData == 0:
                similarityTemp = []
                similarityTemp.append(jellyfish.jaro_distance(i, s))
                '''
                similarityTemp.append(jellyfish.levenshtein_distance(i, s))
                similarityTemp.append(jellyfish.damerau_levenshtein_distance(i, s))
                similarityTemp.append(jellyfish.hamming_distance(i, s))
                similarityTemp.append(jellyfish.jaro_similarity(i, s))
                similarityTemp.append(jellyfish.jaro_winkler_similarity(i, s))
                '''
                #(similarityTemp)
                similarity.append([sum(similarityTemp)/len(similarityTemp), i, j])
            else:
                similarity.append([jellyfish.jaro_distance(i, s), i, idx])
            if len(i) == 1:
                similarity[idx][0] -= 1
            idx += 1

    similarity.sort(reverse=True)
            
    top10 = []
    #('top 10 similar lines')
    for i in range(0, min(len(similarity), 10)):
        #(similarity[i], '\n')
        top10.append(similarity[i])
    return top10


pages = set()


global total_sitemap
total_sitemap = []

def sitemap(wikilink, depth=1, maxdepth=1, cur='START'):    
    global pages    
    global link
    global total_sitemap
  
    html = urlopen(wikilink)
    bsObj = BeautifulSoup(html)
    for links in bsObj.findAll("a"):
        if 'href' in links.attrs:
            try:
                if links.attrs['href'] not in pages:
                    #We have encountered a new page
                    newPage = links.attrs['href']
                    if link not in newPage:
                        #(cur, '->', newPage, depth)
                        total_sitemap.append(cur + '->' + newPage)
                        pages.add(newPage)
                        #if newPage[:5] == 'https':
                        #    return
                        if depth+1 <= maxdepth:
                            sitemap(link+newPage,depth+1,maxdepth, wikilink)
            except:
                print('error')

def get_sitemap(temp_link, depth):
  #(temp_link)
  global total_sitemap
  total_sitemap = []
  sitemap(temp_link, depth)
  return total_sitemap

#search engine: search.ononoki.org

def set_link(nlink):
    global link
    link = nlink              

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
        #sitemap(link)
      get_sitemap(link, 2)
    else:
        return
    menu()


