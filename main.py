from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import jellyfish
import scraper

app = Flask(__name__)
global total_sitemap
total_sitemap = []

pages=set()
def sitemap(wikilink, depth=1, maxdepth=1, cur='START'):    
    global pages    
    global total_sitemap
  
    html = urlopen(wikilink)
    bsObj = BeautifulSoup(html)
    for links in bsObj.findAll("a"):
        if 'href' in links.attrs:
           
                if links.attrs['href'] not in pages:
                    #We have encountered a new page
                    newPage = links.attrs['href']
                    if wikilink not in newPage:
                        print(cur, '->', newPage, depth)
                        strdepth = str(depth)
                        total_sitemap.append([cur + '->' + newPage, strdepth])
                        pages.add(newPage)
                        #if newPage[:5] == 'https':
                        #    return
                        if depth+1 <= maxdepth:
                            sitemap(link+newPage,depth+1,maxdepth, wikilink)
           

def get_sitemap(temp_link, depth):
  print(temp_link)
  sitemap(temp_link, depth)
  print(total_sitemap)
  return total_sitemap

@app.route("/", methods =["GET", "POST"])
def index():
  if request.method == "POST":
      alldata=[]
      gottable,gotlis,gotall=0,0,0
      link = request.form.get("link")
      depth = request.form.get("depth")
      search = request.form.get("search")
      if depth == '':
        depth = 1
      map = get_sitemap(link, int(depth))
      scraper.set_link(link)
      table = scraper.table()
      lis = scraper.lis()
      #if table == '' and lis == '':
      print('SCRAPE ALL')
      alldata = scraper.exall()
      if search != '':
        top10 = scraper.findSimilar(search)
        if table != '':
          gottable=1
        if lis!= '':
          gotlis=1
        gotall=1
        return render_template("results.html", gotmap=1, gottable=gottable,gotlis=gotlis,gotall=gotall,gotsearch=1, map=map, top10=top10,table=table,lis=lis,alldata=alldata)
      else:
        return render_template('results.html', gotmap=1, map=map)
  return render_template('results.html')
  


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
