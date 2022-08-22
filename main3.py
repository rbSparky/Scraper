from urllib.request import urlopen
from bs4 import BeautifulSoup

links = [
        "https://en.wikipedia.org/wiki/Billboard_200",
        "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
        "https://en.wikipedia.org/wiki/List_of_best-selling_music_artists",
        "https://en.wikipedia.org/wiki/List_of_best-selling_video_games",
        "https://en.wikipedia.org/wiki/List_of_best-selling_video_games#List"
        ]

html = urlopen(links[4])
bsObj = BeautifulSoup(html)
#print(str(bsObj.find("table")))
tot = ""

#iterate through all find_alls
#ask user which one they need
for sibling in bsObj.find("ul").li.next_siblings:
     print(sibling)
     tot += str(sibling)
f = open("out3.txt", "w")
f.write(tot)
f.close()

